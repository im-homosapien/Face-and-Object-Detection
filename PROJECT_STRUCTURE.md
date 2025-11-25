# Project Structure

This document provides a detailed overview of the project's file organization and architecture.

## Directory Tree

```
Face-and-Object-tracking/
│
├── 📁 src/                          # Source code
│   ├── 📁 core/                     # Core application logic
│   │   ├── app.py                   # Face recognition app
│   │   ├── unified_app.py           # Unified detection app
│   │   └── __init__.py
│   │
│   ├── 📁 detection/                # Detection modules
│   │   ├── face_detector.py         # DNN face detection
│   │   ├── object_detector.py       # YOLO object detection
│   │   └── __init__.py
│   │
│   ├── 📁 recognition/              # Recognition modules
│   │   ├── face_embedder.py         # DeepFace embeddings
│   │   ├── face_recognizer_v2.py    # Alternative recognizer
│   │   ├── face_tracker.py          # Unknown face tracking
│   │   └── __init__.py
│   │
│   ├── 📁 tracking/                 # Object tracking
│   │   ├── object_tracker.py        # Centroid tracking
│   │   ├── person_tracker.py        # Person ReID
│   │   └── __init__.py
│   │
│   ├── 📁 storage/                  # Data persistence
│   │   ├── face_database.py         # Face database management
│   │   └── __init__.py
│   │
│   ├── 📁 ui/                       # User interface
│   │   ├── renderer.py              # Visual rendering
│   │   ├── input_handler.py         # Keyboard input
│   │   └── __init__.py
│   │
│   ├── main.py                      # Main entry point
│   └── __init__.py
│
├── 📁 models/                       # Pre-trained models
│   ├── deploy.prototxt              # Face detector config
│   ├── res10_300x300_ssd_iter_140000.caffemodel  # Face detector weights
│   ├── yolov4-tiny.cfg              # YOLO config
│   ├── yolov4-tiny.weights          # YOLO weights
│   ├── coco.names                   # Object class names
│   └── .gitkeep
│
├── 📁 docs/                         # Documentation
│   ├── README.md                    # Main documentation
│   ├── QUICK_START.md               # Quick start guide
│   ├── PERFORMANCE_GUIDE.md         # Performance tuning
│   ├── SETUP_COMPLETE.md            # Setup instructions
│   ├── FACE_MATCHING_FIX.md         # Troubleshooting
│   ├── PRESENTATION_GUIDE.md        # Presentation tips
│   └── INSTALLATION_STATUS.md       # Installation info
│
├── 📄 Configuration Files
│   ├── performance_config.py        # Performance settings
│   ├── requirements.txt             # Python dependencies
│   └── .gitignore                   # Git ignore rules
│
├── 🛠️ Utility Scripts
│   ├── test_camera.py               # Camera testing
│   ├── clear_faces.py               # Clear database
│   ├── run_unified.bat              # Quick run script
│   ├── restart_fresh.bat            # Fresh start script
│   ├── push_to_github.bat           # GitHub push helper
│   └── install_dlib.ps1             # dlib installation
│
├── 📋 Project Files
│   ├── LICENSE                      # MIT License
│   ├── CONTRIBUTING.md              # Contribution guidelines
│   ├── CHANGELOG.md                 # Version history
│   ├── GITHUB_PUSH_GUIDE.md         # GitHub guide
│   └── PROJECT_STRUCTURE.md         # This file
│
└── 📊 Generated Files (gitignored)
    ├── face_encodings_advanced.pkl  # Face database
    ├── venv/                        # Virtual environment
    └── __pycache__/                 # Python cache
```

## Module Architecture

### Core Layer
```
┌─────────────────────────────────────────┐
│         Main Entry Point (main.py)      │
│  ┌─────────────┐    ┌────────────────┐ │
│  │ Face Recog  │    │ Unified Mode   │ │
│  │    App      │    │      App       │ │
│  └─────────────┘    └────────────────┘ │
└─────────────────────────────────────────┘
```

### Detection Layer
```
┌──────────────────┐    ┌──────────────────┐
│  Face Detector   │    │ Object Detector  │
│   (DNN/SSD)      │    │   (YOLOv4-tiny)  │
└──────────────────┘    └──────────────────┘
```

### Recognition Layer
```
┌──────────────────┐    ┌──────────────────┐
│  Face Embedder   │    │  Face Tracker    │
│   (DeepFace)     │    │ (Sample Collect) │
└──────────────────┘    └──────────────────┘
```

### Tracking Layer
```
┌──────────────────┐    ┌──────────────────┐
│ Object Tracker   │    │  Person Tracker  │
│   (Centroid)     │    │     (ReID)       │
└──────────────────┘    └──────────────────┘
```

### Storage Layer
```
┌─────────────────────────────────────────┐
│          Face Database (Pickle)         │
│  ┌──────────────┐  ┌─────────────────┐ │
│  │  Embeddings  │  │      Names      │ │
│  └──────────────┘  └─────────────────┘ │
└─────────────────────────────────────────┘
```

### UI Layer
```
┌──────────────────┐    ┌──────────────────┐
│   UI Renderer    │    │  Input Handler   │
│  (Visualization) │    │   (Keyboard)     │
└──────────────────┘    └──────────────────┘
```

## Data Flow

### Face Recognition Flow
```
Camera → Frame Capture → Face Detection → Face Extraction
   ↓
Embedding Extraction → Database Matching → Recognition Result
   ↓
UI Rendering → Display
```

### Object Detection Flow
```
Camera → Frame Capture → Object Detection → NMS Filtering
   ↓
Object Tracking → ID Assignment → Visualization
   ↓
UI Rendering → Display
```

### Face Learning Flow
```
Unknown Face → Sample Collection (20 samples) → Ready Status
   ↓
User Input (Name) → Embedding Averaging → Database Storage
   ↓
Future Recognition
```

## Key Components

### 1. Detection Components
- **FaceDetector**: ResNet-10 SSD for face detection
- **ObjectDetector**: YOLOv4-tiny for object detection

### 2. Recognition Components
- **FaceEmbedder**: DeepFace for embedding extraction
- **FaceTracker**: Tracks unknown faces for learning
- **FaceDatabase**: Persistent storage with pickle

### 3. Tracking Components
- **ObjectTracker**: Centroid-based object tracking
- **PersonTracker**: Person re-identification (ReID)

### 4. UI Components
- **UIRenderer**: Draws bounding boxes and labels
- **InputHandler**: Manages keyboard input

### 5. Configuration
- **performance_config.py**: Tunable parameters
  - Frame skipping interval
  - Frame scaling factor
  - Model selection
  - Thresholds

## File Sizes (Approximate)

| Component | Size | Description |
|-----------|------|-------------|
| Source Code | ~50 KB | All Python files |
| Face Detector Model | ~10 MB | Caffe model |
| YOLO Model | ~24 MB | YOLOv4-tiny weights |
| DeepFace Models | ~580 MB | Downloaded on first run |
| Face Database | ~1-10 KB | Grows with faces |
| Documentation | ~100 KB | All .md files |

## Dependencies

### Core Libraries
- **OpenCV**: Computer vision and video processing
- **DeepFace**: Face recognition framework
- **NumPy**: Numerical operations
- **SciPy**: Scientific computing

### Optional Libraries
- **TensorFlow**: Deep learning backend
- **Keras**: High-level neural networks API
- **dlib**: Face detection and alignment

## Configuration Files

### performance_config.py
```python
PROCESS_EVERY_N_FRAMES = 3  # Frame skipping
FRAME_SCALE = 0.5           # Downscaling
FACE_MODEL = "Facenet"      # Model selection
FACE_MATCH_THRESHOLD = 0.25 # Recognition threshold
```

### requirements.txt
Lists all Python package dependencies with versions.

### .gitignore
Excludes unnecessary files from version control:
- Virtual environments
- Python cache
- Model weights
- Face database
- IDE files

## Development Workflow

1. **Setup**: Install dependencies, download models
2. **Development**: Modify source code in `src/`
3. **Testing**: Run `test_camera.py`, test features
4. **Configuration**: Adjust `performance_config.py`
5. **Documentation**: Update relevant .md files
6. **Commit**: Use git to track changes
7. **Push**: Upload to GitHub

## Best Practices

### Code Organization
- Keep modules focused and single-purpose
- Use clear, descriptive names
- Add docstrings to all functions
- Follow PEP 8 style guide

### Performance
- Profile before optimizing
- Use frame skipping for speed
- Downscale frames when possible
- Choose appropriate models

### Documentation
- Update README for new features
- Add inline comments for complex logic
- Keep CHANGELOG.md current
- Document configuration changes

---

For more information, see the main [README.md](README.md) or [CONTRIBUTING.md](CONTRIBUTING.md).
