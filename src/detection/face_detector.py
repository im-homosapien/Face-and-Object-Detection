"""
Face Detector Module - DNN-based Face Detection

This module implements face detection using OpenCV's DNN module with a
pre-trained Caffe model (ResNet-10 SSD). The detector is fast, accurate,
and works well in various lighting conditions.

Model Details:
    - Architecture: Single Shot Detector (SSD) with ResNet-10 backbone
    - Input: 300x300 RGB image
    - Output: Face bounding boxes with confidence scores
    - Pre-trained on: Large-scale face dataset

Features:
    - High accuracy face detection
    - Robust to lighting variations
    - Handles multiple faces per frame
    - Configurable confidence threshold
    - Automatic model download

Performance:
    - Fast inference (~10-30ms per frame on CPU)
    - Suitable for real-time applications
    - Works well with frame downscaling

Usage:
    detector = FaceDetector(confidence_threshold=0.5)
    faces = detector.detect(frame)  # Returns list of (x1, y1, x2, y2, confidence)

Author: Face & Object Detection System
Version: 2.0
"""

import cv2
import os
import urllib.request


class FaceDetector:
    """
    Detects faces in images using OpenCV DNN with ResNet-10 SSD.
    
    This class provides a simple interface for face detection using a
    pre-trained deep neural network. It automatically downloads the
    required model files on first use.
    
    Attributes:
        confidence_threshold (float): Minimum confidence for valid detection (0.0-1.0)
        detector (cv2.dnn.Net): Loaded DNN model for face detection
    
    Model Files:
        - deploy.prototxt: Network architecture definition
        - res10_300x300_ssd_iter_140000.caffemodel: Pre-trained weights (~10MB)
    """
    
    def __init__(self, confidence_threshold=0.5):
        """
        Initialize face detector with confidence threshold.
        
        Loads the pre-trained DNN model for face detection. If model files
        are not present, they will be automatically downloaded from OpenCV's
        GitHub repository.
        
        Args:
            confidence_threshold (float): Minimum confidence score for a detection
                to be considered valid. Range: 0.0 to 1.0
                - Lower values: More detections, more false positives
                - Higher values: Fewer detections, fewer false positives
                - Recommended: 0.5 for balanced performance
        
        Raises:
            Exception: If model files cannot be downloaded or loaded
        """
        self.confidence_threshold = confidence_threshold
        self.detector = self._load_model()
    
    def _load_model(self):
        """
        Load DNN face detection model from disk or download if needed.
        
        This method handles model file management:
        1. Creates models directory if it doesn't exist
        2. Checks for required model files
        3. Downloads missing files from OpenCV repository
        4. Loads the Caffe model into OpenCV DNN
        
        Model Files:
            - deploy.prototxt: Network architecture (~5KB)
            - res10_300x300_ssd_iter_140000.caffemodel: Weights (~10MB)
        
        Returns:
            cv2.dnn.Net: Loaded face detection model
            
        Raises:
            Exception: If download or loading fails
        """
        # Create models directory
        model_dir = "models"
        os.makedirs(model_dir, exist_ok=True)
        
        # Define model file paths
        prototxt_path = os.path.join(model_dir, "deploy.prototxt")
        model_path = os.path.join(model_dir, "res10_300x300_ssd_iter_140000.caffemodel")
        
        # Download architecture file if missing
        if not os.path.exists(prototxt_path):
            print("Downloading face detector config...")
            url = "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt"
            urllib.request.urlretrieve(url, prototxt_path)
        
        # Download weights file if missing
        if not os.path.exists(model_path):
            print("Downloading face detector weights...")
            url = "https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel"
            urllib.request.urlretrieve(url, model_path)
        
        # Load Caffe model
        detector = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
        print("✓ Face detector loaded")
        return detector
    
    def detect(self, frame):
        """
        Detect faces in a frame using DNN.
        
        This method performs face detection on the input frame:
        1. Resizes frame to 300x300 (model input size)
        2. Creates blob with mean subtraction for normalization
        3. Runs forward pass through network
        4. Filters detections by confidence threshold
        5. Scales coordinates back to original frame size
        6. Ensures bounding boxes are within frame bounds
        
        Args:
            frame (numpy.ndarray): BGR image from OpenCV (any size)
            
        Returns:
            list: List of detected faces, each as tuple:
                (x1, y1, x2, y2, confidence)
                - x1, y1: Top-left corner coordinates
                - x2, y2: Bottom-right corner coordinates
                - confidence: Detection confidence score (0.0-1.0)
        
        Notes:
            - Mean values (104.0, 177.0, 123.0) are for BGR normalization
            - Model expects 300x300 input but works with any frame size
            - Coordinates are scaled back to original frame dimensions
        """
        h, w = frame.shape[:2]
        
        # Create blob from image
        # - Resize to 300x300 (model input size)
        # - Scale factor: 1.0 (no scaling)
        # - Mean subtraction: (104.0, 177.0, 123.0) for BGR channels
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 
            1.0, 
            (300, 300), 
            (104.0, 177.0, 123.0)
        )
        
        # Run forward pass through network
        self.detector.setInput(blob)
        detections = self.detector.forward()
        
        # Process detections
        faces = []
        for i in range(detections.shape[2]):
            # Extract confidence score
            confidence = detections[0, 0, i, 2]
            
            # Filter by confidence threshold
            if confidence > self.confidence_threshold:
                # Extract bounding box coordinates (normalized 0-1)
                box = detections[0, 0, i, 3:7] * [w, h, w, h]
                x1, y1, x2, y2 = box.astype("int")
                
                # Ensure coordinates are within frame bounds
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)
                
                faces.append((x1, y1, x2, y2, confidence))
        
        return faces
