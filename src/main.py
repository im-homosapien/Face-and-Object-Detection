"""
Main Entry Point for Face & Object Detection System

This is the primary entry point for the detection system. It provides a menu-driven
interface allowing users to choose between three operational modes:
1. Face Recognition Only - Optimized for face detection and identification
2. Object Detection Only - Detects and tracks 80+ object types using YOLO
3. Unified Mode - Combines both face recognition and object detection

The system uses modular architecture with separate components for detection,
recognition, tracking, storage, and UI rendering.

Usage:
    python src/main.py
    
Then select the desired mode (1-3) from the menu.

Author: Face & Object Detection System
Version: 2.0
"""

import sys
import traceback

# Add src directory to Python path for module imports
sys.path.insert(0, 'src')

from core import FaceRecognitionApp, UnifiedApp


def main():
    """
    Main entry point function.
    
    Displays a menu for mode selection and initializes the appropriate
    application instance based on user choice. Handles graceful shutdown
    on keyboard interrupt and displays error messages for exceptions.
    
    Modes:
        1: Face Recognition Only - Uses FaceRecognitionApp
        2: Object Detection Only - Uses UnifiedApp with face recognition disabled
        3: Unified Mode - Uses UnifiedApp with both features enabled
    
    Returns:
        None
        
    Raises:
        KeyboardInterrupt: Caught and handled gracefully
        Exception: Caught and error details printed with traceback
    """
    # Display menu
    print("=" * 60)
    print("Detection System")
    print("=" * 60)
    print("1. Face Recognition Only")
    print("2. Object Detection Only")
    print("3. Unified (Face + Object Detection)")
    print("=" * 60)
    
    # Get user choice
    choice = input("Enter choice (1-3): ").strip()
    
    try:
        # Initialize and run the appropriate application
        if choice == "1":
            # Face recognition only mode
            app = FaceRecognitionApp()
            app.run()
        elif choice == "2":
            # Object detection only mode
            app = UnifiedApp(enable_face_recognition=False, enable_object_detection=True)
            app.run()
        elif choice == "3":
            # Unified mode with both features
            app = UnifiedApp(enable_face_recognition=True, enable_object_detection=True)
            app.run()
        else:
            print("Invalid choice")
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nInterrupted by user")
    except Exception as e:
        # Handle any other exceptions
        print(f"Error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
