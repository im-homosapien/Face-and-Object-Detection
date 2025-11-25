"""
Camera Test Utility - Verify Webcam Functionality

This utility script tests webcam access and functionality before running
the main detection system. It helps diagnose camera-related issues.

What It Tests:
    - Camera device availability (index 0 and 1)
    - Camera opening capability
    - Frame capture functionality
    - Frame dimensions and format

Test Procedure:
    1. Attempts to open camera at index 0 (default)
    2. If successful, captures and displays a test frame
    3. If failed, tries camera at index 1 (secondary)
    4. Reports results and suggests troubleshooting steps

Common Issues Detected:
    - Camera in use by another application
    - Missing camera permissions
    - No camera connected
    - Outdated camera drivers
    - Wrong camera index

Usage:
    python test_camera.py

Expected Output (Success):
    Testing camera access...
    Trying camera index 0...
    ✓ Camera 0 opened successfully!
    ✓ Frame captured: (480, 640, 3)
    Camera is working! Press any key in the window to close.

Expected Output (Failure):
    Testing camera access...
    Trying camera index 0...
    ✗ Failed to open camera 0
    Trying camera index 1...
    ✗ Failed to open camera 1
    Possible issues:
    1. Camera is being used by another application
    ...

Troubleshooting:
    - Close other apps using camera (Zoom, Skype, etc.)
    - Check camera permissions in system settings
    - Verify camera is connected (for external cameras)
    - Update camera drivers
    - Try different camera index (0, 1, 2)

Author: Face & Object Detection System
Version: 2.0
"""

import cv2

# Start camera test
print("Testing camera access...")
print("\nTrying camera index 0...")

# Attempt to open default camera (index 0)
cap = cv2.VideoCapture(0)

if cap.isOpened():
    # Camera opened successfully
    print("✓ Camera 0 opened successfully!")
    
    # Try to capture a frame
    ret, frame = cap.read()
    
    if ret:
        # Frame captured successfully
        print(f"✓ Frame captured: {frame.shape}")
        print("\nCamera is working! Press any key in the window to close.")
        
        # Display test frame
        cv2.imshow('Camera Test', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        # Frame capture failed
        print("✗ Failed to read frame")
    
    # Release camera
    cap.release()
else:
    # Camera 0 failed, try camera 1
    print("✗ Failed to open camera 0")
    print("\nTrying camera index 1...")
    
    cap = cv2.VideoCapture(1)
    
    if cap.isOpened():
        # Camera 1 opened successfully
        print("✓ Camera 1 opened successfully!")
        
        # Try to capture a frame
        ret, frame = cap.read()
        
        if ret:
            # Frame captured successfully
            print(f"✓ Frame captured: {frame.shape}")
            print("\nCamera is working! Press any key in the window to close.")
            
            # Display test frame
            cv2.imshow('Camera Test', frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        # Release camera
        cap.release()
    else:
        # Both cameras failed
        print("✗ Failed to open camera 1")
        print("\nPossible issues:")
        print("1. Camera is being used by another application")
        print("2. Camera permissions not granted")
        print("3. No camera connected")
        print("4. Camera drivers need update")

print("\nTest complete.")
