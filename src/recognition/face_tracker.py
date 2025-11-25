"""
Face Tracker Module - Unknown Face Tracking and Sample Collection

This module tracks unknown faces across frames and collects multiple samples
before allowing the user to name them. This multi-sample approach improves
recognition accuracy by capturing faces from different angles and expressions.

Key Features:
    - Tracks unknown faces across frames using embeddings
    - Collects multiple samples per face for robust learning
    - Assigns unique IDs to each unknown face
    - Determines when enough samples are collected
    - Prevents duplicate tracking of the same face

How It Works:
    1. Unknown face detected → Extract embedding
    2. Check if embedding matches existing tracked face
    3. If match: Add to existing face's samples
    4. If no match: Create new tracked face with unique ID
    5. When samples_needed reached: Mark face as "ready" for naming
    6. User names face → Samples added to database

Benefits of Multi-Sample Collection:
    - More robust recognition (averages out variations)
    - Captures different angles and expressions
    - Reduces false matches
    - Improves long-term recognition accuracy

Usage:
    tracker = FaceTracker(samples_needed=20)
    face_id, count, ready = tracker.track(embedding)
    if ready:
        samples = tracker.get_embeddings(face_id)
        database.add_person(name, samples)

Author: Face & Object Detection System
Version: 2.0
"""

import numpy as np
from collections import defaultdict


class FaceTracker:
    """
    Tracks unknown faces and collects samples for training.
    
    This class maintains a collection of unknown faces, each identified by
    a unique ID, and accumulates multiple embedding samples for each face.
    When enough samples are collected, the face is marked as "ready" for
    naming by the user.
    
    Attributes:
        samples_needed (int): Number of samples required before naming
        similarity_threshold (float): Distance threshold for matching faces
        unknown_faces (defaultdict): Maps face_id to list of embeddings
        face_id_counter (int): Counter for generating unique face IDs
    
    Tracking Strategy:
        - Uses embedding similarity to match faces across frames
        - Maintains separate sample collections for each unique face
        - Prevents duplicate tracking of the same person
        - Allows multiple unknown faces to be tracked simultaneously
    """
    
    def __init__(self, samples_needed=10, similarity_threshold=0.5):
        """
        Initialize face tracker with collection parameters.
        
        Args:
            samples_needed (int): Number of embedding samples to collect
                before marking a face as ready for naming.
                - Lower values: Faster learning, less robust
                - Higher values: Slower learning, more robust
                - Recommended: 10-20 samples
                - Default: 10
            
            similarity_threshold (float): Maximum distance for considering
                two embeddings as the same face.
                - Lower values: Stricter matching (may create duplicates)
                - Higher values: Looser matching (may merge different people)
                - Recommended: 0.5 for DeepFace models
                - Default: 0.5
        
        Notes:
            - Each tracked face gets a unique ID starting from 0
            - Samples are stored as embedding vectors
            - Multiple faces can be tracked simultaneously
        """
        self.samples_needed = samples_needed
        self.similarity_threshold = similarity_threshold
        self.unknown_faces = defaultdict(list)  # {face_id: [embeddings]}
        self.face_id_counter = 0  # Increments for each new face
    
    def track(self, embedding):
        """
        Track an unknown face embedding and collect samples.
        
        This method is called for each unknown face detection. It determines
        if the face belongs to an existing tracked face or is a new face,
        then adds the embedding to the appropriate collection.
        
        Tracking Logic:
        1. Compare embedding with all existing tracked faces
        2. If match found (distance < threshold): Add to existing face
        3. If no match: Create new tracked face with unique ID
        4. Increment sample count for the face
        5. Check if enough samples collected (ready for naming)
        
        Args:
            embedding (numpy.ndarray): Face embedding vector from FaceEmbedder
        
        Returns:
            tuple: (face_id, sample_count, is_ready)
                - face_id (int): Unique identifier for this face
                - sample_count (int): Number of samples collected so far
                - is_ready (bool): True if samples_needed threshold reached
        
        Example:
            >>> tracker = FaceTracker(samples_needed=10)
            >>> face_id, count, ready = tracker.track(embedding)
            >>> print(f"Face {face_id}: {count}/10 samples, Ready: {ready}")
            Face 0: 5/10 samples, Ready: False
        
        Notes:
            - Same face detected multiple times will have same face_id
            - Different faces get different face_ids
            - Ready status triggers UI prompt for naming
        """
        # Find if this embedding belongs to an existing tracked face
        face_id = self._find_face_id(embedding)
        
        if face_id is None:
            # New unknown face - assign new ID
            face_id = self.face_id_counter
            self.face_id_counter += 1
        
        # Add embedding to this face's sample collection
        self.unknown_faces[face_id].append(embedding)
        
        # Calculate current status
        sample_count = len(self.unknown_faces[face_id])
        is_ready = sample_count >= self.samples_needed
        
        return face_id, sample_count, is_ready
    
    def _find_face_id(self, embedding):
        """
        Find if an embedding belongs to an existing tracked face.
        
        Compares the given embedding with all embeddings of all tracked faces.
        If any comparison yields a distance below the similarity threshold,
        the face is considered a match.
        
        Args:
            embedding (numpy.ndarray): Face embedding to match
        
        Returns:
            int or None: face_id if match found, None if no match
        
        Algorithm:
            - Iterate through all tracked faces
            - For each face, compare with all its embeddings
            - If any distance < threshold: Return face_id
            - If no matches: Return None
        
        Notes:
            - Uses cosine distance for comparison
            - First match wins (doesn't find best match)
            - Threshold determines strictness of matching
        """
        from .face_embedder import FaceEmbedder
        
        # Check each tracked face
        for face_id, embeddings in self.unknown_faces.items():
            # Compare with each sample of this face
            for known_embedding in embeddings:
                distance = FaceEmbedder.compare(embedding, known_embedding)
                if distance < self.similarity_threshold:
                    return face_id
        
        # No match found
        return None
    
    def get_embeddings(self, face_id):
        """
        Get all collected embeddings for a specific face.
        
        Used when user names a face to retrieve all samples for
        adding to the database.
        
        Args:
            face_id (int): Unique identifier of the tracked face
        
        Returns:
            list: List of embedding vectors (numpy arrays)
        
        Example:
            >>> embeddings = tracker.get_embeddings(face_id)
            >>> database.add_person("John", embeddings)
        """
        return self.unknown_faces[face_id]
    
    def remove_face(self, face_id):
        """
        Remove a tracked face from the tracker.
        
        Called after a face has been named and added to the database,
        or if tracking needs to be cancelled.
        
        Args:
            face_id (int): Unique identifier of the face to remove
        
        Notes:
            - Silently succeeds if face_id doesn't exist
            - Frees memory by removing all collected samples
            - Face ID is not reused
        """
        if face_id in self.unknown_faces:
            del self.unknown_faces[face_id]
