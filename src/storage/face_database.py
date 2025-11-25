"""
Face Database Module - Persistent Face Storage and Retrieval

This module manages the persistent storage of known faces and their embeddings.
It provides functionality for adding new faces, finding matches, and maintaining
a database file that persists across application runs.

Database Structure:
    - embeddings: List of averaged face embedding vectors
    - names: List of corresponding person names
    - Stored as pickle file for fast serialization

Features:
    - Persistent storage (survives application restarts)
    - Fast embedding-based matching
    - Automatic saving on updates
    - Multi-sample averaging for robustness
    - Configurable matching threshold

Matching Algorithm:
    1. Compare query embedding with all stored embeddings
    2. Calculate cosine distance for each comparison
    3. Find minimum distance
    4. If distance < threshold: Return matched name
    5. If distance >= threshold: Return None (unknown)

File Format:
    - Format: Python pickle (.pkl)
    - Contents: Dictionary with 'embeddings' and 'names' keys
    - Location: Project root directory
    - Default: face_encodings_advanced.pkl

Usage:
    database = FaceDatabase()
    database.add_person("John", [emb1, emb2, emb3])
    name, distance = database.find_match(query_embedding)

Author: Face & Object Detection System
Version: 2.0
"""

import pickle
import numpy as np
import os


class FaceDatabase:
    """
    Manages persistent storage and retrieval of face embeddings.
    
    This class handles all database operations for known faces, including
    loading from disk, saving to disk, adding new faces, and finding matches.
    Each person is represented by an averaged embedding vector computed from
    multiple samples.
    
    Attributes:
        database_file (str): Path to the pickle file storing face data
        embeddings (list): List of averaged face embedding vectors
        names (list): List of person names (parallel to embeddings)
    
    Database Operations:
        - Load: Read existing faces from disk on initialization
        - Save: Write updated faces to disk after changes
        - Add: Add new person with multiple sample embeddings
        - Match: Find best matching person for a query embedding
        - Query: Get list of known names and counts
    """
    
    def __init__(self, database_file="face_encodings_advanced.pkl"):
        """
        Initialize face database and load existing data.
        
        Creates a new database if the file doesn't exist, or loads
        existing faces if the file is present.
        
        Args:
            database_file (str): Path to the pickle file for storing faces.
                Default: "face_encodings_advanced.pkl"
                The file will be created in the project root directory.
        
        File Structure:
            {
                'embeddings': [array1, array2, ...],  # Averaged embeddings
                'names': ['John', 'Jane', ...]         # Corresponding names
            }
        
        Notes:
            - Automatically loads existing database on initialization
            - Creates empty database if file doesn't exist
            - Prints status message during loading
        """
        self.database_file = database_file
        self.embeddings = []  # List of averaged embedding vectors
        self.names = []       # List of corresponding person names
        self._load()          # Load existing data from disk
    
    def _load(self):
        """
        Load existing face data from disk.
        
        Internal method called during initialization to load previously
        saved faces from the pickle file. If the file doesn't exist,
        initializes with empty lists.
        
        File Format:
            Dictionary with keys:
            - 'embeddings': List of numpy arrays (averaged embeddings)
            - 'names': List of strings (person names)
        
        Side Effects:
            - Sets self.embeddings and self.names
            - Prints status message
        
        Error Handling:
            - Silently creates empty database if file doesn't exist
            - May raise exception if file is corrupted
        """
        if os.path.exists(self.database_file):
            print(f"Loading face database from {self.database_file}...")
            with open(self.database_file, 'rb') as f:
                data = pickle.load(f)
                self.embeddings = data['embeddings']
                self.names = data['names']
            print(f"✓ Loaded {len(self.names)} known faces")
        else:
            print("No existing database - starting fresh")
    
    def save(self):
        """
        Save current face data to disk.
        
        Serializes the embeddings and names to a pickle file for persistent
        storage. Called automatically after adding new faces.
        
        File Contents:
            {
                'embeddings': [array1, array2, ...],
                'names': ['John', 'Jane', ...]
            }
        
        Notes:
            - Overwrites existing file
            - Uses pickle for fast serialization
            - File is binary format
            - Atomic write (no partial saves)
        """
        data = {
            'embeddings': self.embeddings,
            'names': self.names
        }
        with open(self.database_file, 'wb') as f:
            pickle.dump(data, f)
    
    def add_person(self, name, embeddings_list):
        """
        Add a new person to the database with multiple samples.
        
        This method takes multiple embedding samples for a person and
        averages them to create a robust representation. Averaging reduces
        the impact of outliers and variations in pose/expression.
        
        Process:
        1. Average all embedding samples
        2. Add averaged embedding to database
        3. Add name to database
        4. Save database to disk
        5. Print confirmation
        
        Args:
            name (str): Person's name (identifier)
            embeddings_list (list): List of embedding vectors (numpy arrays)
                from multiple face samples of the same person
        
        Example:
            >>> samples = [emb1, emb2, emb3, emb4, emb5]
            >>> database.add_person("John Doe", samples)
            ✓ Added John Doe with 5 samples
        
        Notes:
            - More samples = more robust recognition
            - Averaging handles pose/expression variations
            - Automatically saves to disk
            - Name should be unique (no duplicate checking)
        """
        # Average all embeddings for robustness
        # This reduces impact of outliers and variations
        avg_embedding = np.mean(embeddings_list, axis=0)
        
        # Add to database
        self.embeddings.append(avg_embedding)
        self.names.append(name)
        
        # Persist to disk
        self.save()
        
        print(f"✓ Added {name} with {len(embeddings_list)} samples")
    
    def find_match(self, embedding, threshold=0.25):
        """
        Find the best matching person for a query embedding.
        
        Compares the query embedding with all known faces in the database
        using cosine distance. Returns the name of the best match if the
        distance is below the threshold, otherwise returns None.
        
        Matching Algorithm:
        1. Calculate distance to each known face
        2. Find minimum distance
        3. If min_distance < threshold: Return matched name
        4. Otherwise: Return None (unknown face)
        
        Args:
            embedding (numpy.ndarray): Query face embedding to match
            threshold (float): Maximum distance for a valid match
                - Lower: Stricter matching (fewer false positives)
                - Higher: Looser matching (more false positives)
                - Facenet recommended: 0.20-0.30
                - VGG-Face recommended: 0.40-0.60
                - Default: 0.25 (strict for Facenet)
        
        Returns:
            tuple: (name, distance)
                - name (str or None): Matched person's name, or None if no match
                - distance (float): Distance to best match (or min distance if no match)
        
        Example:
            >>> name, dist = database.find_match(query_emb, threshold=0.25)
            >>> if name:
            >>>     print(f"Matched: {name} (distance: {dist:.3f})")
            >>> else:
            >>>     print(f"Unknown face (closest: {dist:.3f})")
        
        Performance:
            - O(n) where n = number of known faces
            - Fast for small databases (<1000 faces)
            - Consider indexing for large databases
        """
        # Handle empty database
        if not self.embeddings:
            return None, 1.0
        
        from recognition.face_embedder import FaceEmbedder
        
        # Calculate distances to all known faces
        distances = []
        for known_embedding in self.embeddings:
            distance = FaceEmbedder.compare(embedding, known_embedding)
            distances.append(distance)
        
        # Find best match
        min_distance = min(distances)
        
        # Check if match is good enough
        if min_distance < threshold:
            index = distances.index(min_distance)
            return self.names[index], min_distance
        
        # No match found
        return None, min_distance
    
    def get_known_names(self):
        """
        Get list of all known person names.
        
        Returns a copy of the names list to prevent external modification.
        
        Returns:
            list: Copy of all person names in the database
        
        Example:
            >>> names = database.get_known_names()
            >>> print(f"Known people: {', '.join(names)}")
            Known people: John, Jane, Bob
        """
        return self.names.copy()
    
    def count(self):
        """
        Get the number of known faces in the database.
        
        Returns:
            int: Number of people in the database
        
        Example:
            >>> print(f"Database contains {database.count()} faces")
            Database contains 5 faces
        """
        return len(self.names)
