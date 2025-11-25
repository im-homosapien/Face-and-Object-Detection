"""
Face Embedder Module - Deep Learning Face Embeddings

This module extracts face embeddings (numerical representations) using
DeepFace, a state-of-the-art face recognition framework. Embeddings are
high-dimensional vectors that capture unique facial features.

Supported Models:
    - Facenet: 128 dimensions, fastest, good accuracy
    - Facenet512: 512 dimensions, balanced speed and accuracy
    - VGG-Face: 2622 dimensions, slowest, best accuracy
    - ArcFace: 512 dimensions, fast with high accuracy

How Face Embeddings Work:
    1. Face image is fed into a deep neural network
    2. Network extracts high-level facial features
    3. Features are compressed into a fixed-size vector (embedding)
    4. Similar faces have similar embeddings (small distance)
    5. Different faces have different embeddings (large distance)

Distance Metrics:
    - Cosine distance: Measures angle between vectors
    - Range: 0.0 (identical) to 2.0 (opposite)
    - Typical threshold: 0.20-0.30 for Facenet, 0.40-0.60 for VGG-Face

Performance Comparison:
    Model       | Speed      | Accuracy   | Dimensions | Use Case
    ------------|------------|------------|------------|------------------
    Facenet     | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐   | 128        | Real-time systems
    Facenet512  | ⚡⚡⚡⚡   | ⭐⭐⭐⭐⭐ | 512        | Balanced
    ArcFace     | ⚡⚡⚡⚡   | ⭐⭐⭐⭐⭐ | 512        | High accuracy
    VGG-Face    | ⚡⚡       | ⭐⭐⭐⭐⭐ | 2622       | Best accuracy

Usage:
    embedder = FaceEmbedder(model_name="Facenet")
    embedding = embedder.extract(face_image)
    distance = FaceEmbedder.compare(embedding1, embedding2)

Author: Face & Object Detection System
Version: 2.0
"""

import cv2
import numpy as np
from deepface import DeepFace
import warnings

# Suppress DeepFace warnings for cleaner output
warnings.filterwarnings('ignore')


class FaceEmbedder:
    """
    Extracts face embeddings using DeepFace framework.
    
    This class provides a simple interface for extracting face embeddings
    using various pre-trained deep learning models. Embeddings are numerical
    representations of faces that can be compared for recognition.
    
    Attributes:
        model_name (str): Name of the model to use (Facenet, VGG-Face, etc.)
        embedding_sizes (dict): Mapping of model names to embedding dimensions
    
    Models:
        - Facenet: Fast, 128D, good for real-time
        - Facenet512: Balanced, 512D, better accuracy
        - VGG-Face: Slow, 2622D, best accuracy
        - ArcFace: Fast, 512D, high accuracy
    """
    
    def __init__(self, model_name="Facenet"):
        """
        Initialize face embedder with specified model.
        
        The model will be automatically downloaded on first use if not
        already cached. Model files are stored in ~/.deepface/weights/
        
        Args:
            model_name (str): Name of the face recognition model to use.
                Options: "Facenet", "Facenet512", "VGG-Face", "ArcFace"
                Default: "Facenet" (fastest, good accuracy)
        
        Model Selection Guide:
            - Facenet: Best for real-time, low-end systems (128D)
            - Facenet512: Balanced performance (512D)
            - VGG-Face: Best accuracy, slower (2622D)
            - ArcFace: High accuracy, good speed (512D)
        """
        self.model_name = model_name
        print(f"✓ Using DeepFace for face recognition ({self.model_name} model)")
        
        # Embedding dimensions for each model
        # Used for creating zero vectors on extraction failure
        self.embedding_sizes = {
            "VGG-Face": 2622,   # Largest, most accurate
            "Facenet": 128,     # Smallest, fastest
            "Facenet512": 512,  # Balanced
            "ArcFace": 512      # High accuracy
        }
    
    def extract(self, face_image):
        """
        Extract face embedding from a face image.
        
        This method processes a cropped face image and extracts a numerical
        embedding vector that represents the unique facial features. The
        embedding can be compared with other embeddings for recognition.
        
        Processing Steps:
        1. Resize face to 160x160 for faster processing (if larger)
        2. Convert from BGR (OpenCV) to RGB (DeepFace requirement)
        3. Pass through deep learning model
        4. Extract embedding vector from model output
        5. Return as numpy array
        
        Args:
            face_image (numpy.ndarray): Cropped face image in BGR format
                (from OpenCV). Can be any size, will be resized if needed.
        
        Returns:
            numpy.ndarray: Face embedding vector
                - Facenet: 128-dimensional vector
                - Facenet512: 512-dimensional vector
                - VGG-Face: 2622-dimensional vector
                - ArcFace: 512-dimensional vector
                
                Returns zero vector if extraction fails.
        
        Notes:
            - Resizing to 160x160 provides 2x speedup with minimal accuracy loss
            - enforce_detection=False: Skip face detection (already done)
            - detector_backend='skip': Don't run detector again
            - Handles extraction failures gracefully
        
        Performance:
            - Facenet: ~20-50ms per face
            - VGG-Face: ~100-200ms per face
        """
        try:
            # Resize face for faster processing
            # Facenet works well with 160x160, larger sizes don't improve accuracy much
            if face_image.shape[0] > 160 or face_image.shape[1] > 160:
                face_image = cv2.resize(face_image, (160, 160))
            
            # Convert BGR (OpenCV format) to RGB (DeepFace requirement)
            face_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
            
            # Extract embedding using DeepFace
            embedding_objs = DeepFace.represent(
                img_path=face_rgb,
                model_name=self.model_name,
                enforce_detection=False,  # We already detected the face
                detector_backend='skip'   # Skip detection, use provided image
            )
            
            # Extract the embedding vector from result
            embedding = np.array(embedding_objs[0]["embedding"])
            return embedding
            
        except Exception as e:
            # Handle extraction failures gracefully
            print(f"DeepFace extraction failed: {e}")
            # Return a zero vector of appropriate size
            embedding_size = self.embedding_sizes.get(self.model_name, 128)
            return np.zeros(embedding_size)
    
    @staticmethod
    def compare(embedding1, embedding2):
        """
        Compare two face embeddings using cosine distance.
        
        Cosine distance measures the angle between two vectors in high-dimensional
        space. It's ideal for face recognition because it's invariant to vector
        magnitude and focuses on directional similarity.
        
        Distance Interpretation:
            - 0.0: Identical faces (same person, same photo)
            - 0.0-0.3: Very similar (likely same person)
            - 0.3-0.6: Somewhat similar (might be same person)
            - 0.6-1.0: Different (likely different people)
            - 1.0-2.0: Very different (definitely different people)
        
        Recommended Thresholds:
            - Facenet: 0.20-0.30 (stricter matching)
            - Facenet512: 0.25-0.35
            - VGG-Face: 0.40-0.60 (more lenient)
            - ArcFace: 0.25-0.35
        
        Args:
            embedding1 (numpy.ndarray): First face embedding vector
            embedding2 (numpy.ndarray): Second face embedding vector
        
        Returns:
            float: Cosine distance between embeddings
                - 0.0: Identical
                - Higher values: More different
                - 1.0: Orthogonal (completely different)
                - 2.0: Opposite direction (maximum difference)
        
        Formula:
            cosine_distance = 1 - (dot(v1, v2) / (||v1|| * ||v2||))
        
        Notes:
            - Returns 1.0 if either embedding is zero vector
            - Handles edge cases gracefully
            - Fast computation (single dot product and norms)
        """
        # Calculate dot product of the two vectors
        dot_product = np.dot(embedding1, embedding2)
        
        # Calculate L2 norms (magnitudes) of each vector
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        # Handle zero vectors (invalid embeddings)
        if norm1 == 0 or norm2 == 0:
            return 1.0
        
        # Calculate cosine similarity: dot(v1, v2) / (||v1|| * ||v2||)
        # Range: -1 (opposite) to 1 (identical)
        cosine_similarity = dot_product / (norm1 * norm2)
        
        # Convert to cosine distance: 1 - similarity
        # Range: 0 (identical) to 2 (opposite)
        cosine_distance = 1 - cosine_similarity
        
        return cosine_distance
