"""
Performance Configuration for Face & Object Detection System

Adjust these settings to balance speed vs accuracy based on your hardware.
"""

# ============================================================
# FRAME PROCESSING
# ============================================================

# Process every N frames (higher = faster but less smooth)
# Recommended: 2-3 for decent hardware, 4-5 for slower systems
PROCESS_EVERY_N_FRAMES = 3

# Frame scale for processing (lower = faster but less accurate)
# Recommended: 0.5 (half size) for good balance
# Try 0.4 for slower systems, 0.6-0.7 for better accuracy
FRAME_SCALE = 0.5

# ============================================================
# FACE RECOGNITION MODEL
# ============================================================

# Choose face recognition model:
# - "Facenet": Fastest, 128 dimensions, good accuracy
# - "Facenet512": Balanced, 512 dimensions, better accuracy
# - "VGG-Face": Slowest, 2622 dimensions, best accuracy
# - "ArcFace": Fast, 512 dimensions, very good accuracy
FACE_MODEL = "Facenet"

# Face image resize for embedding extraction
# Smaller = faster, but may reduce accuracy
# Recommended: 160 for Facenet, 224 for VGG-Face
FACE_RESIZE = 160

# ============================================================
# DETECTION THRESHOLDS
# ============================================================

# Face detection confidence (0.0 to 1.0)
# Lower = more detections but more false positives
FACE_CONFIDENCE_THRESHOLD = 0.5

# Object detection confidence (0.0 to 1.0)
OBJECT_CONFIDENCE_THRESHOLD = 0.4

# Face recognition match threshold
# Lower = stricter matching (fewer false matches)
# Higher = more lenient (may match different people)
# Facenet: 0.20-0.30 (recommended: 0.25)
# VGG-Face: 0.40-0.60 (recommended: 0.50)
FACE_MATCH_THRESHOLD = 0.25

# ============================================================
# TRACKING
# ============================================================

# Number of face samples needed before allowing naming
# Lower = faster learning, higher = more accurate
FACE_SAMPLES_NEEDED = 20

# Maximum frames an object can disappear before being removed
OBJECT_MAX_DISAPPEARED = 20
PERSON_MAX_DISAPPEARED = 50

# ============================================================
# PERFORMANCE TIPS
# ============================================================
"""
For SLOW systems:
- PROCESS_EVERY_N_FRAMES = 5
- FRAME_SCALE = 0.4
- FACE_MODEL = "Facenet"
- FACE_RESIZE = 128

For FAST systems:
- PROCESS_EVERY_N_FRAMES = 2
- FRAME_SCALE = 0.6
- FACE_MODEL = "Facenet512" or "ArcFace"
- FACE_RESIZE = 160

For BEST ACCURACY (slow):
- PROCESS_EVERY_N_FRAMES = 1
- FRAME_SCALE = 1.0
- FACE_MODEL = "VGG-Face"
- FACE_RESIZE = 224
"""
