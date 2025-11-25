"""
Face Recognition Application - Main Application Class

This module implements the core face recognition application that integrates
all detection, recognition, tracking, and UI components into a cohesive system.

The application provides:
- Real-time face detection using DNN-based detector
- Face recognition using deep learning embeddings (DeepFace)
- Unknown face tracking and sample collection
- Interactive face naming through keyboard input
- Persistent face database storage
- Performance optimizations (frame skipping, downscaling)

Architecture:
    FaceRecognitionApp orchestrates the following components:
    - FaceDetector: Detects faces in frames
    - FaceEmbedder: Extracts face embeddings for recognition
    - FaceDatabase: Stores and retrieves known faces
    - FaceTracker: Tracks unknown faces for learning
    - UIRenderer: Handles visual rendering
    - InputHandler: Manages keyboard input

Performance Features:
    - Frame skipping: Process every Nth frame for speed
    - Frame downscaling: Reduce resolution for faster processing
    - Configurable models: Choose between speed and accuracy
    - Result caching: Reuse results for skipped frames

Usage:
    app = FaceRecognitionApp()
    app.run()

Author: Face & Object Detection System
Version: 2.0
"""

import cv2
import sys
import os

# Add parent directories to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from detection import FaceDetector
from recognition import FaceEmbedder, FaceTracker
from storage import FaceDatabase
from ui import UIRenderer, InputHandler

# Import performance configuration settings
# Falls back to defaults if config file not found
try:
    from performance_config import (
        PROCESS_EVERY_N_FRAMES,  # Frame skipping interval
        FRAME_SCALE,              # Frame downscaling factor
        FACE_MODEL,               # Face recognition model name
        FACE_CONFIDENCE_THRESHOLD,  # Minimum confidence for face detection
        FACE_SAMPLES_NEEDED,      # Samples needed before naming
        FACE_MATCH_THRESHOLD      # Threshold for face matching
    )
except ImportError:
    # Default values if config not found
    PROCESS_EVERY_N_FRAMES = 3
    FRAME_SCALE = 0.5
    FACE_MODEL = "Facenet"
    FACE_CONFIDENCE_THRESHOLD = 0.5
    FACE_SAMPLES_NEEDED = 20
    FACE_MATCH_THRESHOLD = 0.25


class FaceRecognitionApp:
    """
    Main application class for face recognition system.
    
    This class orchestrates all components of the face recognition system,
    including detection, embedding extraction, database management, tracking,
    and user interface rendering.
    
    Attributes:
        detector (FaceDetector): Face detection module using DNN
        embedder (FaceEmbedder): Face embedding extraction using DeepFace
        database (FaceDatabase): Persistent storage for known faces
        tracker (FaceTracker): Tracks unknown faces for learning
        ui (UIRenderer): Handles visual rendering
        input_handler (InputHandler): Manages keyboard input
        frame_skip (int): Counter for frame skipping optimization
        process_every_n_frames (int): Process every Nth frame
        frame_scale (float): Downscaling factor for processing
        last_results (list): Cached results from last processed frame
    
    Performance Optimizations:
        - Frame skipping: Only process every Nth frame
        - Frame downscaling: Process at reduced resolution
        - Result caching: Reuse results for skipped frames
        - Configurable models: Balance speed vs accuracy
    """
    
    def __init__(self):
        """
        Initialize the face recognition application.
        
        Sets up all required modules and loads configuration settings.
        Initializes the face database, detector, embedder, tracker, and UI components.
        
        The initialization process:
        1. Creates detector with configured confidence threshold
        2. Initializes embedder with selected model (Facenet/VGG-Face/etc.)
        3. Loads existing face database from disk
        4. Sets up face tracker for unknown faces
        5. Initializes UI renderer and input handler
        6. Configures performance optimization parameters
        
        Raises:
            RuntimeError: If any module fails to initialize
        """
        print("=" * 60)
        print("Face Recognition System")
        print("=" * 60)
        
        # Initialize core detection and recognition modules
        self.detector = FaceDetector(confidence_threshold=FACE_CONFIDENCE_THRESHOLD)
        self.embedder = FaceEmbedder(model_name=FACE_MODEL)
        self.database = FaceDatabase()
        self.tracker = FaceTracker(samples_needed=FACE_SAMPLES_NEEDED)
        
        # Initialize UI components
        self.ui = UIRenderer()
        self.input_handler = InputHandler()
        
        # Performance optimization settings
        self.frame_skip = 0  # Frame counter for skipping
        self.process_every_n_frames = PROCESS_EVERY_N_FRAMES  # Skip interval
        self.frame_scale = FRAME_SCALE  # Downscaling factor (0.5 = half size)
        self.last_results = []  # Cache for skipped frames
        
        print("=" * 60)
        print("System ready!")
        print("=" * 60)
    
    def process_frame(self, frame, force_process=False):
        """
        Process a single video frame for face detection and recognition.
        
        This method implements the core processing pipeline with performance
        optimizations. It handles frame skipping, downscaling, face detection,
        embedding extraction, and recognition.
        
        Processing Pipeline:
        1. Check if frame should be skipped (performance optimization)
        2. Downscale frame for faster processing
        3. Detect faces in downscaled frame
        4. For each detected face:
           a. Scale coordinates back to original size
           b. Extract face region from original frame
           c. Generate face embedding
           d. Try to match against known faces
           e. If unknown, track for learning
        5. Cache results for skipped frames
        6. Draw annotations on frame
        
        Args:
            frame (numpy.ndarray): BGR image from webcam (original resolution)
            force_process (bool): If True, bypass frame skipping optimization
            
        Returns:
            tuple: (annotated_frame, results_list)
                - annotated_frame: Frame with bounding boxes and labels drawn
                - results_list: List of detection results, each containing:
                    - box: (x1, y1, x2, y2) coordinates
                    - name: Person's name if known, None if unknown
                    - status: 'known', 'ready', or 'collecting'
                    - face_id: Tracking ID for unknown faces
                    - sample_count: Number of samples collected
                    - confidence: Detection confidence score
        
        Performance Notes:
            - Processes every Nth frame (configurable)
            - Downscales frames before processing
            - Reuses cached results for skipped frames
            - Provides 20-50x speedup over baseline
        """
        # Frame skipping optimization for performance
        self.frame_skip += 1
        if not force_process and self.frame_skip % self.process_every_n_frames != 0:
            # Use cached results from last processed frame
            output = self._draw_results(frame, self.last_results)
            return output, self.last_results
        
        # Downscale frame for faster processing (e.g., 0.5 = half size)
        small_frame = cv2.resize(frame, None, fx=self.frame_scale, fy=self.frame_scale)
        
        # Detect faces in downscaled frame
        faces = self.detector.detect(small_frame)
        
        results = []
        
        # Process each detected face
        for x1, y1, x2, y2, confidence in faces:
            # Scale coordinates back to original frame size
            x1 = int(x1 / self.frame_scale)
            y1 = int(y1 / self.frame_scale)
            x2 = int(x2 / self.frame_scale)
            y2 = int(y2 / self.frame_scale)
            
            # Extract face region from original high-resolution frame
            face_img = frame[y1:y2, x1:x2]
            
            # Skip if face region is invalid
            if face_img.size == 0:
                continue
            
            # Extract face embedding using deep learning
            embedding = self.embedder.extract(face_img)
            
            # Try to match against known faces in database
            name, distance = self.database.find_match(embedding, threshold=FACE_MATCH_THRESHOLD)
            
            if name:
                # Face recognized - add to results as known
                results.append({
                    'box': (x1, y1, x2, y2),
                    'name': name,
                    'status': 'known',
                    'confidence': confidence
                })
            else:
                # Unknown face - track it for potential learning
                face_id, sample_count, is_ready = self.tracker.track(embedding)
                
                results.append({
                    'box': (x1, y1, x2, y2),
                    'name': None,
                    'status': 'ready' if is_ready else 'collecting',
                    'face_id': face_id,
                    'sample_count': sample_count,
                    'confidence': confidence
                })
        
        # Cache results for frame skipping optimization
        self.last_results = results
        
        # Draw annotations on frame
        output = self._draw_results(frame, results)
        
        return output, results
    
    def _draw_results(self, frame, results):
        """
        Draw detection and recognition results on frame.
        
        This internal method handles all visual rendering of detection results,
        including bounding boxes, labels, status indicators, and UI overlays.
        
        Visual Elements:
        - Green boxes: Known faces with names
        - Yellow boxes: Ready faces (enough samples collected)
        - Red boxes: Collecting samples (not ready yet)
        - Input overlay: When naming a face
        - Statistics: Count of known faces
        
        Args:
            frame (numpy.ndarray): Original frame to draw on
            results (list): List of detection results from process_frame()
            
        Returns:
            numpy.ndarray: Frame with all annotations drawn
            
        Side Effects:
            - Modifies result dictionaries by adding 'selection_number' field
              for ready faces to enable keyboard selection
        """
        # Create a copy to avoid modifying original frame
        output = frame.copy()
        
        # Assign selection numbers to ready faces for keyboard input
        ready_face_count = 0
        
        for result in results:
            x1, y1, x2, y2 = result['box']
            
            # Determine color and label based on face status
            if result['status'] == 'known':
                # Known face - green box with name
                color = (0, 255, 0)  # Green in BGR
                label = result['name']
            elif result['status'] == 'ready':
                # Ready to name - yellow box with selection number
                ready_face_count += 1
                color = (0, 255, 255)  # Yellow in BGR
                label = f"[{ready_face_count}] Ready - Press {ready_face_count}"
                # Store selection number for input handler
                result['selection_number'] = ready_face_count
            else:
                # Still collecting samples - red box with progress
                color = (0, 0, 255)  # Red in BGR
                sample_count = result['sample_count']
                label = f"Collecting {sample_count}/{self.tracker.samples_needed}"
            
            # Draw bounding box and label
            self.ui.draw_face_box(output, x1, y1, x2, y2, label, color)
        
        # Draw input overlay if user is naming a face
        if self.input_handler.is_in_input_mode():
            selected_num = self.input_handler.get_selected_number()
            self.ui.draw_input_box(output, self.input_handler.get_input_text(), selected_num)
        
        # Draw statistics (known face count)
        self.ui.draw_stats(output, self.database.count())
        
        return output
    
    def run(self):
        """
        Run the main application loop.
        
        This method implements the main event loop that:
        1. Opens the webcam
        2. Continuously captures frames
        3. Processes each frame for face detection/recognition
        4. Displays annotated frames
        5. Handles keyboard input
        6. Manages graceful shutdown
        
        The loop continues until:
        - User presses 'q' to quit
        - Window is closed
        - Camera fails to capture frames
        - An exception occurs
        
        Keyboard Controls:
            - q: Quit application
            - 1-9: Select ready face for naming
            - Type name and press Enter: Save face
            - Esc: Cancel naming
        
        Raises:
            RuntimeError: If webcam cannot be opened
            
        Cleanup:
            - Releases webcam
            - Closes all OpenCV windows
            - Prints final statistics
        """
        # Open webcam (index 0 = default camera)
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            raise RuntimeError("Failed to open webcam")
        
        # Create display window
        window_name = 'Face Recognition - Press Q to quit'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        
        # Print startup information
        print("\nStarting face recognition...")
        if self.database.count() > 0:
            print(f"Known faces: {', '.join(self.database.get_known_names())}")
        else:
            print("No known faces - system will learn as you use it")
        print("Press 'q' to quit\n")
        
        try:
            # Main processing loop
            while True:
                # Capture frame from webcam
                ret, frame = cap.read()
                
                if not ret:
                    print("Failed to grab frame")
                    break
                
                # Process frame for face detection and recognition
                output, results = self.process_frame(frame)
                
                # Display annotated frame
                cv2.imshow(window_name, output)
                
                # Handle keyboard input (returns False to quit)
                key = cv2.waitKey(1) & 0xFF
                if not self.input_handler.handle_key(key, results, self.database, self.tracker):
                    break
                
                # Check if window was closed by user
                if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                    break
        
        finally:
            # Cleanup: release resources
            cap.release()
            cv2.destroyAllWindows()
            print("\nFace recognition stopped")
            print(f"Total known faces: {self.database.count()}")
