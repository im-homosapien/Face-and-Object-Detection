"""
Clear Face Database Utility - Reset Face Recognition Database

This utility script deletes the face database file, allowing you to start
fresh with face recognition. Useful for testing, troubleshooting, or when
you want to remove all learned faces.

What It Does:
    - Deletes the face_encodings_advanced.pkl file
    - Removes all known faces from the system
    - Allows starting with a clean slate
    - Preserves model files and configuration

When to Use:
    - Testing with different faces
    - Removing incorrectly named faces
    - Starting over after threshold changes
    - Troubleshooting recognition issues
    - Clearing old/outdated face data

What Gets Deleted:
    - All known face names
    - All face embeddings
    - Face database file (face_encodings_advanced.pkl)

What Gets Preserved:
    - Model files (in models/ directory)
    - Configuration settings (performance_config.py)
    - Application code
    - DeepFace model cache

Safety:
    - Only deletes the database file
    - No other files are affected
    - Can be run multiple times safely
    - Reversible by re-learning faces

Usage:
    python clear_faces.py

Expected Output (Database Exists):
    ✓ Cleared face database: face_encodings_advanced.pkl
    You can now start fresh and add faces again.
    The new stricter threshold (0.25) will prevent false matches.
    
    Run the application to start learning faces:
      python src/main.py

Expected Output (No Database):
    No database file found: face_encodings_advanced.pkl
    Database is already empty.
    
    Run the application to start learning faces:
      python src/main.py

After Running:
    - All faces will be unknown
    - System will collect samples for new faces
    - Previous names are lost (cannot be recovered)
    - Face recognition starts from scratch

Author: Face & Object Detection System
Version: 2.0
"""

import os

# Database file path
database_file = "face_encodings_advanced.pkl"

# Check if database file exists
if os.path.exists(database_file):
    # Delete the database file
    os.remove(database_file)
    print(f"✓ Cleared face database: {database_file}")
    print("\nYou can now start fresh and add faces again.")
    print("The new stricter threshold (0.25) will prevent false matches.")
else:
    # Database file doesn't exist
    print(f"No database file found: {database_file}")
    print("Database is already empty.")

# Instructions for next steps
print("\nRun the application to start learning faces:")
print("  python src/main.py")
