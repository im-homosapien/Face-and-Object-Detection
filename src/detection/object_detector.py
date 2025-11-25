"""
Object Detector Module - YOLOv4-tiny Object Detection

This module implements real-time object detection using YOLOv4-tiny,
a fast and accurate object detection model. It can detect 80 different
object classes from the COCO dataset.

Model Details:
    - Architecture: YOLOv4-tiny (lightweight version of YOLOv4)
    - Input: 416x416 RGB image
    - Output: Bounding boxes, class labels, confidence scores
    - Classes: 80 COCO classes (person, car, dog, laptop, etc.)
    - Model Size: ~24MB

Features:
    - Real-time object detection
    - 80+ object classes
    - Non-maximum suppression for clean results
    - Configurable confidence threshold
    - Automatic model download
    - Color-coded visualization

Performance:
    - Faster than full YOLOv4
    - Suitable for real-time applications
    - Good balance of speed and accuracy
    - CPU-optimized

COCO Classes Include:
    person, bicycle, car, motorcycle, airplane, bus, train, truck, boat,
    traffic light, fire hydrant, stop sign, parking meter, bench, bird,
    cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe, backpack,
    umbrella, handbag, tie, suitcase, frisbee, skis, snowboard, sports ball,
    kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket,
    bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple,
    sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake, chair,
    couch, potted plant, bed, dining table, toilet, tv, laptop, mouse,
    remote, keyboard, cell phone, microwave, oven, toaster, sink,
    refrigerator, book, clock, vase, scissors, teddy bear, hair drier,
    toothbrush

Usage:
    detector = ObjectDetector(confidence_threshold=0.4)
    objects = detector.detect(frame)  # Returns list of (x1, y1, x2, y2, class, conf)

Author: Face & Object Detection System
Version: 2.0
"""

import cv2
import numpy as np
import os
import urllib.request


class ObjectDetector:
    """
    Detects objects in images using YOLOv4-tiny.
    
    This class provides a simple interface for object detection using
    YOLOv4-tiny, a fast and accurate object detection model. It automatically
    downloads required model files on first use.
    
    Attributes:
        confidence_threshold (float): Minimum confidence for valid detection
        nms_threshold (float): Non-maximum suppression threshold
        net (cv2.dnn.Net): Loaded YOLO model
        classes (list): List of 80 COCO class names
        output_layers (list): Names of YOLO output layers
        colors (numpy.ndarray): Random colors for each class
    
    Model Files:
        - yolov4-tiny.weights: Pre-trained weights (~24MB)
        - yolov4-tiny.cfg: Network configuration
        - coco.names: Class names file
    """
    
    def __init__(self, confidence_threshold=0.4, nms_threshold=0.4):
        """
        Initialize object detector with YOLOv4-tiny.
        
        Loads the pre-trained YOLOv4-tiny model for object detection.
        If model files are not present, they will be automatically
        downloaded from the official Darknet repository.
        
        Args:
            confidence_threshold (float): Minimum confidence score for a
                detection to be considered valid. Range: 0.0 to 1.0
                - Lower values: More detections, more false positives
                - Higher values: Fewer detections, fewer false positives
                - Recommended: 0.4 for balanced performance
            
            nms_threshold (float): Non-maximum suppression threshold for
                removing overlapping bounding boxes. Range: 0.0 to 1.0
                - Lower values: More aggressive suppression
                - Higher values: Keep more overlapping boxes
                - Recommended: 0.4 for clean results
        
        Raises:
            Exception: If model files cannot be downloaded or loaded
        """
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold
        
        # Load model and class names
        self.net, self.classes, self.output_layers = self._load_model()
        
        # Generate random colors for each class (for visualization)
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        
        # Set backend for better performance
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        
        print(f"✓ YOLOv4 detector initialized with {len(self.classes)} classes")
    
    def _load_model(self):
        """Load YOLOv4-tiny model and class names."""
        model_dir = "models"
        os.makedirs(model_dir, exist_ok=True)
        
        # Paths for YOLOv4-tiny
        weights_path = os.path.join(model_dir, "yolov4-tiny.weights")
        config_path = os.path.join(model_dir, "yolov4-tiny.cfg")
        names_path = os.path.join(model_dir, "coco.names")
        
        # Delete old YOLOv3 files if they exist
        old_files = [
            os.path.join(model_dir, "yolov3-tiny.weights"),
            os.path.join(model_dir, "yolov3-tiny.cfg")
        ]
        for old_file in old_files:
            if os.path.exists(old_file):
                os.remove(old_file)
                print(f"Removed old file: {old_file}")
        
        # Download YOLOv4-tiny files if needed
        if not os.path.exists(weights_path):
            print("Downloading YOLOv4-tiny weights (better accuracy)...")
            url = "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights"
            urllib.request.urlretrieve(url, weights_path)
            print("✓ Weights downloaded")
        
        if not os.path.exists(config_path):
            print("Downloading YOLOv4-tiny config...")
            url = "https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg"
            urllib.request.urlretrieve(url, config_path)
            print("✓ Config downloaded")
        
        if not os.path.exists(names_path):
            print("Downloading class names...")
            url = "https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names"
            urllib.request.urlretrieve(url, names_path)
            print("✓ Class names downloaded")
        
        # Load YOLOv4
        net = cv2.dnn.readNet(weights_path, config_path)
        
        # Load class names
        with open(names_path, 'r') as f:
            classes = [line.strip() for line in f.readlines()]
        
        # Get output layer names
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        
        return net, classes, output_layers
    
    def detect(self, frame):
        """
        Detect objects in a frame.
        
        Args:
            frame: BGR image (numpy array)
            
        Returns:
            List of detected objects [(x1, y1, x2, y2, class_name, confidence), ...]
        """
        h, w = frame.shape[:2]
        
        # Create blob
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        
        # Forward pass
        self.net.setInput(blob)
        outputs = self.net.forward(self.output_layers)
        
        # Process detections
        boxes = []
        confidences = []
        class_ids = []
        
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                if confidence > self.confidence_threshold:
                    # Get box coordinates
                    center_x = int(detection[0] * w)
                    center_y = int(detection[1] * h)
                    width = int(detection[2] * w)
                    height = int(detection[3] * h)
                    
                    x1 = int(center_x - width / 2)
                    y1 = int(center_y - height / 2)
                    
                    boxes.append([x1, y1, width, height])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        
        # Apply non-maximum suppression
        results = []
        
        if len(boxes) > 0:
            indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, self.nms_threshold)
            
            if len(indices) > 0:
                for i in indices.flatten():
                    x1, y1, width, height = boxes[i]
                    x2 = x1 + width
                    y2 = y1 + height
                    
                    # Ensure within bounds
                    x1, y1 = max(0, x1), max(0, y1)
                    x2, y2 = min(w, x2), min(h, y2)
                    
                    class_name = self.classes[class_ids[i]]
                    confidence = confidences[i]
                    
                    results.append((x1, y1, x2, y2, class_name, confidence))
        
        return results
    
    def get_color(self, class_name):
        """Get color for a class."""
        if class_name in self.classes:
            idx = self.classes.index(class_name)
            return tuple(map(int, self.colors[idx]))
        return (255, 255, 255)
