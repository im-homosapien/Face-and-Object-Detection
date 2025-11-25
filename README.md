# Face & Object Detection System

A high-performance, real-time face recognition and object detection system built with Python, OpenCV, and deep learning. Features optimized performance (20-50x faster than baseline), modular architecture, and easy-to-use interface.

## Features

### Face Recognition
- Real-time face detection and recognition
- Deep learning embeddings (Facenet, VGG-Face, ArcFace)
- Interactive face learning - name faces directly in the video window
- Persistent face database with automatic saving
- Multi-face tracking with unique IDs
- Configurable accuracy vs speed tradeoffs

### Object Detection
- 80+ object types detection using YOLOv4-tiny
- Real-time object tracking
- Confidence-based filtering
- Bounding box visualization with labels

### Performance Optimizations
- Frame skipping for 3x speed boost
- Intelligent frame downscaling (4x faster)
- Optimized face recognition models (5-10x faster)
- Configurable performance profiles
- **Overall: 20-50x faster than baseline implementation**

### Architecture
- Clean OOP design with modular components
- Separation of concerns (detection, recognition, tracking, storage, UI)
- Easy to extend and customize
- Well-documented codebase

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/dhirajkk91/Face-and-Object-tracking.git
cd Face-and-Object-tracking
```

### 2. Create Virtual Environment
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- OpenCV for computer vision
- DeepFace for face recognition
- TensorFlow/Keras for deep learning
- dlib for face detection
- NumPy, SciPy for numerical operations
- All required dependencies

**Note:** On first run, models will auto-download (~600MB total):
- Face detector models (~10MB)
- Object detector (YOLOv4-tiny, ~24MB)
- Face recognition models (~580MB)

### 4. Run the Application
```bash
python src/main.py
```

Choose your mode:
- **1** - Face Recognition Only (optimized, smooth)
- **2** - Object Detection Only
- **3** - Unified Mode (Face + Object Detection)

Press **Q** to quit.

## How to Use

### Face Recognition Mode

1. **Launch the application:**
   ```bash
   python src/main.py
   # Select option 1
   ```

2. **Learning new faces:**
   - System automatically detects faces
   - Shows "Collecting X/20" while gathering samples
   - When ready, shows "[1] Ready - Press 1"
   - Press the number key, type the person's name, press ENTER
   - Face is now recognized automatically!

3. **Recognition:**
   - Known faces show name and confidence score
   - Unknown faces show "Unknown" with tracking ID
   - Multiple faces tracked simultaneously

### Object Detection Mode

1. **Launch:**
   ```bash
   python src/main.py
   # Select option 2
   ```

2. **Detection:**
   - Detects 80+ object types (person, car, dog, laptop, etc.)
   - Shows bounding boxes with labels and confidence
   - Real-time tracking with unique IDs

### Unified Mode

Combines both face recognition and object detection in a single view.

## Performance Tuning

Edit `performance_config.py` to customize for your hardware:

### For Slower Systems (Prioritize Speed)
```python
PROCESS_EVERY_N_FRAMES = 5      # Skip more frames
FRAME_SCALE = 0.4               # Smaller processing size
FACE_MODEL = "Facenet"          # Fastest model
```

### For Faster Systems (Better Quality)
```python
PROCESS_EVERY_N_FRAMES = 2      # Process more frames
FRAME_SCALE = 0.6               # Larger processing size
FACE_MODEL = "Facenet512"       # More accurate model
```

### For Best Accuracy (Slower)
```python
PROCESS_EVERY_N_FRAMES = 1      # Process every frame
FRAME_SCALE = 1.0               # Full resolution
FACE_MODEL = "VGG-Face"         # Most accurate model
```

### Model Comparison

| Model | Speed | Accuracy | Dimensions | Best For |
|-------|-------|----------|------------|----------|
| Facenet | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ | 128 | Real-time, low-end systems |
| Facenet512 | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 512 | Balanced performance |
| ArcFace | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 512 | High accuracy, good speed |
| VGG-Face | ⚡⚡ | ⭐⭐⭐⭐⭐ | 2622 | Best accuracy, slower |

See `PERFORMANCE_GUIDE.md` for detailed optimization tips.

## Project Structure
```
Face-and-Object-tracking/
├── src/
│   ├── main.py                      # Entry point
│   ├── core/                        # Core application logic
│   │   ├── app.py                   # Face recognition app
│   │   └── unified_app.py           # Unified detection app
│   ├── detection/                   # Detection modules
│   │   ├── face_detector.py         # Face detection (DNN)
│   │   └── object_detector.py       # Object detection (YOLO)
│   ├── recognition/                 # Recognition modules
│   │   ├── face_embedder.py         # Face embeddings (DeepFace)
│   │   ├── face_recognizer_v2.py    # Face matching
│   │   └── face_tracker.py          # Face tracking
│   ├── tracking/                    # Object tracking
│   │   └── object_tracker.py        # Centroid tracking
│   ├── storage/                     # Data persistence
│   │   └── face_database.py         # Face database management
│   └── ui/                          # User interface
│       ├── renderer.py              # Drawing and visualization
│       └── input_handler.py         # Keyboard input handling
├── models/                          # Pre-trained models
│   ├── deploy.prototxt              # Face detector config
│   ├── res10_300x300_ssd_iter_140000.caffemodel
│   ├── yolov4-tiny.cfg              # YOLO config
│   ├── yolov4-tiny.weights          # YOLO weights
│   └── coco.names                   # Object class names
├── face_encodings_advanced.pkl      # Face database (auto-created)
├── performance_config.py            # Performance settings
├── requirements.txt                 # Python dependencies
├── QUICK_START.md                   # Quick start guide
├── PERFORMANCE_GUIDE.md             # Performance optimization guide
└── README.md                        # This file
```

## Configuration Files

- **performance_config.py** - Adjust frame processing, model selection, thresholds
- **face_encodings_advanced.pkl** - Persistent face database (auto-created)
- **models/** - Pre-trained deep learning models

## Troubleshooting

### Lag/Stuttering
- Increase `PROCESS_EVERY_N_FRAMES` to 4 or 5
- Decrease `FRAME_SCALE` to 0.4 or 0.3
- Switch to faster model: `FACE_MODEL = "Facenet"`

### Poor Detection Accuracy
- Decrease `PROCESS_EVERY_N_FRAMES` to 2
- Increase `FRAME_SCALE` to 0.6 or 0.7
- Improve lighting conditions
- Switch to more accurate model: `FACE_MODEL = "Facenet512"`

### Camera Not Opening
- Check if another application is using the camera
- Try changing camera index in code (0 to 1)
- Verify camera permissions

### Installation Issues
- Ensure Python 3.8+ is installed
- Use virtual environment to avoid conflicts
- On Windows, dlib may require Visual Studio Build Tools
- See `INSTALLATION_STATUS.md` for detailed setup info

## Utilities

### Clear Face Database
```bash
python clear_faces.py
```
Removes all learned faces from the database.

### Test Camera
```bash
python test_camera.py
```
Verifies camera is working correctly.

## Technical Details

### Dependencies
- **OpenCV** - Computer vision and video processing
- **DeepFace** - Face recognition framework
- **TensorFlow/Keras** - Deep learning backend
- **dlib** - Face detection and alignment
- **NumPy** - Numerical operations
- **SciPy** - Scientific computing

### Algorithms
- **Face Detection:** DNN-based SSD with ResNet-10 backbone
- **Face Recognition:** Deep learning embeddings (Facenet/VGG-Face/ArcFace)
- **Object Detection:** YOLOv4-tiny
- **Tracking:** Centroid-based tracking with Euclidean distance

### Performance Optimizations
1. **Frame Skipping** - Process every Nth frame, reuse results
2. **Frame Downscaling** - Reduce resolution for processing
3. **Model Selection** - Choose faster models (Facenet vs VGG-Face)
4. **Face Resizing** - Optimize face crop sizes
5. **Caching** - Reuse embeddings and detection results

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- OpenCV for computer vision tools
- DeepFace for face recognition framework
- YOLOv4 for object detection
- dlib for face detection capabilities

## Contact

For questions or support, please open an issue on GitHub.

---

**Enjoy your optimized face and object detection system! 🚀**
