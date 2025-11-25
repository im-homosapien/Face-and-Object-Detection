"""
UI Renderer Module - Visual Rendering and Display

This module handles all visual rendering for the detection system, including
drawing bounding boxes, labels, overlays, and statistics on video frames.

Features:
    - Face bounding boxes with color-coded status
    - Object bounding boxes with class labels
    - Interactive input overlay for naming faces
    - Statistics display (face count, object count)
    - Clean, professional visual design

Color Coding:
    - Green: Known faces (recognized)
    - Yellow: Ready faces (enough samples collected)
    - Red: Collecting faces (still gathering samples)
    - Cyan: ReID faces (recognized via person tracking)
    - Random: Objects (each class has unique color)

Visual Elements:
    - Bounding boxes: 2px thickness for visibility
    - Labels: White text on colored background
    - Input overlay: Semi-transparent black background
    - Statistics: Top-left corner, green text

Design Principles:
    - High contrast for visibility
    - Consistent styling across elements
    - Non-intrusive overlays
    - Clear status indicators

Usage:
    renderer = UIRenderer()
    renderer.draw_face_box(frame, x1, y1, x2, y2, "John", (0, 255, 0))
    renderer.draw_stats(frame, known_count=5)

Author: Face & Object Detection System
Version: 2.0
"""

import cv2


class UIRenderer:
    """
    Handles drawing UI elements on video frames.
    
    This class provides static methods for rendering various UI components
    including bounding boxes, labels, overlays, and statistics. All methods
    modify frames in-place for efficiency.
    
    Methods:
        - draw_face_box: Draw face bounding box with label
        - draw_object_box: Draw object bounding box with label
        - draw_input_box: Draw interactive naming overlay
        - draw_stats: Draw face recognition statistics
        - draw_unified_stats: Draw combined statistics
    
    Notes:
        - All methods are static (no instance needed)
        - Frames are modified in-place
        - Uses OpenCV drawing functions
        - Coordinates are in pixels (x, y)
    """
    
    @staticmethod
    def draw_face_box(frame, x1, y1, x2, y2, label, color):
        """
        Draw a face bounding box with label.
        
        Renders a rectangular bounding box around a detected face with a
        colored label bar at the bottom containing the person's name or status.
        
        Visual Design:
            - Rectangle: 2px border in specified color
            - Label bar: Filled rectangle at bottom of face box
            - Text: White, centered in label bar
        
        Args:
            frame (numpy.ndarray): Image to draw on (modified in-place)
            x1 (int): Left edge of bounding box
            y1 (int): Top edge of bounding box
            x2 (int): Right edge of bounding box
            y2 (int): Bottom edge of bounding box
            label (str): Text to display (name or status)
            color (tuple): BGR color tuple (B, G, R)
                - Green (0, 255, 0): Known face
                - Yellow (0, 255, 255): Ready to name
                - Red (0, 0, 255): Collecting samples
        
        Example:
            >>> renderer.draw_face_box(frame, 100, 100, 200, 200, "John", (0, 255, 0))
        
        Notes:
            - Label bar height: 35 pixels
            - Text offset: 6 pixels from left, 6 pixels from bottom
            - Font: Hershey Simplex, size 0.6, thickness 2
        """
        # Draw bounding box rectangle
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        # Draw filled label background bar
        cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), color, cv2.FILLED)
        
        # Draw label text (white on colored background)
        cv2.putText(frame, label, (x1 + 6, y2 - 6),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    @staticmethod
    def draw_input_box(frame, input_text, face_number=0):
        """
        Draw interactive input overlay for naming faces.
        
        Displays a semi-transparent overlay at the bottom of the frame
        with instructions and a text input field for entering a person's name.
        
        Visual Design:
            - Semi-transparent black background (70% opacity)
            - Yellow title text
            - White input text with cursor
            - Gray instruction text
        
        Args:
            frame (numpy.ndarray): Image to draw on (modified in-place)
            input_text (str): Current text input from user
            face_number (int): Number of the face being named (1-9)
        
        Layout:
            - Position: Bottom center of frame
            - Size: Full width minus 100px margins, 100px height
            - Title: "Naming Face #N"
            - Input: "Name: [text]_"
            - Help: "Press ENTER to save | ESC to cancel"
        
        Example:
            >>> renderer.draw_input_box(frame, "Joh", face_number=1)
            # Displays: "Naming Face #1" with "Name: Joh_"
        
        Notes:
            - Cursor shown as underscore after text
            - Overlay doesn't block face visibility
            - Instructions guide user interaction
        """
        h, w = frame.shape[:2]
        
        # Create semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (50, h - 150), (w - 50, h - 50), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Draw title text (yellow)
        cv2.putText(frame, f"Naming Face #{face_number}", (70, h - 120),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # Draw input text with cursor (white)
        cv2.putText(frame, f"Name: {input_text}_", (70, h - 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Draw instruction text (gray)
        cv2.putText(frame, "Press ENTER to save | ESC to cancel", (70, h - 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    @staticmethod
    def draw_stats(frame, known_count):
        """
        Draw face recognition statistics on frame.
        
        Displays the number of known faces in the database at the
        top-left corner of the frame.
        
        Args:
            frame (numpy.ndarray): Image to draw on (modified in-place)
            known_count (int): Number of known faces in database
        
        Visual Design:
            - Position: Top-left (10, 30)
            - Color: Green (0, 255, 0)
            - Font: Hershey Simplex, size 0.7, thickness 2
        
        Example:
            >>> renderer.draw_stats(frame, known_count=5)
            # Displays: "Known: 5"
        """
        cv2.putText(frame, f'Known: {known_count}', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    @staticmethod
    def draw_object_box(frame, x1, y1, x2, y2, label, color):
        """
        Draw an object bounding box with label.
        
        Renders a rectangular bounding box around a detected object with
        a colored label bar at the top containing the class name and
        confidence score.
        
        Visual Design:
            - Rectangle: 2px border in class-specific color
            - Label bar: Filled rectangle at top of object box
            - Text: White, left-aligned in label bar
        
        Args:
            frame (numpy.ndarray): Image to draw on (modified in-place)
            x1 (int): Left edge of bounding box
            y1 (int): Top edge of bounding box
            x2 (int): Right edge of bounding box
            y2 (int): Bottom edge of bounding box
            label (str): Text to display (e.g., "ID:5 car: 0.95")
            color (tuple): BGR color tuple (class-specific)
        
        Example:
            >>> renderer.draw_object_box(frame, 100, 100, 300, 200, 
            ...                          "ID:1 car: 0.95", (255, 0, 0))
        
        Notes:
            - Label bar size adapts to text length
            - Label positioned above bounding box
            - Font: Hershey Simplex, size 0.5, thickness 2
        """
        # Draw bounding box rectangle
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        # Calculate label size for background
        label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        
        # Draw filled label background bar (above box)
        cv2.rectangle(frame, (x1, y1 - label_size[1] - 10), 
                     (x1 + label_size[0], y1), color, cv2.FILLED)
        
        # Draw label text (white on colored background)
        cv2.putText(frame, label, (x1, y1 - 5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    @staticmethod
    def draw_unified_stats(frame, face_count, object_count):
        """
        Draw unified statistics for combined detection mode.
        
        Displays counts of both detected faces and objects at the
        top-left corner of the frame.
        
        Args:
            frame (numpy.ndarray): Image to draw on (modified in-place)
            face_count (int): Number of known faces in database
            object_count (int): Number of objects currently detected
        
        Visual Design:
            - Position: Top-left (10, 30)
            - Color: Green (0, 255, 0)
            - Font: Hershey Simplex, size 0.7, thickness 2
            - Format: "Faces: N | Objects: M"
        
        Example:
            >>> renderer.draw_unified_stats(frame, face_count=5, object_count=3)
            # Displays: "Faces: 5 | Objects: 3"
        """
        cv2.putText(frame, f'Faces: {face_count} | Objects: {object_count}', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
