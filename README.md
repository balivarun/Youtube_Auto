# YouTube Hand Gesture Control

Control YouTube video playback using hand gestures detected through your webcam.

## Features

- **Fist (Closed Hand)**: Pause/Play video
- **Open Hand (All Fingers Extended)**: Play/Pause video  
- **Thumbs Up**: Fast-forward 10 seconds
- **Pinky Up**: Rewind 10 seconds

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## Usage

1. Open YouTube in your browser and start playing a video
2. Make sure the YouTube tab stays active/focused
3. Run the Python application: `python main.py`
4. Position your hand in front of the webcam with good lighting
5. Hold gestures steady for 1 second to trigger actions
6. Press 'q' in the camera window to quit

## Requirements

- Python 3.8+ (tested on Python 3.13)
- Webcam
- Active YouTube tab in browser
- Good lighting for hand detection

## Tips for Better Detection

- Use contrasting background behind your hand
- Ensure good lighting conditions
- Hold gestures steady for at least 1 second
- Position hand clearly in camera view
- Keep YouTube tab focused for keyboard shortcuts to work

## Troubleshooting

- **Camera not working**: Ensure webcam isn't used by other applications
- **Gestures not recognized**: Improve lighting, use contrasting background
- **YouTube not responding**: Make sure YouTube tab is active/focused
- **Erratic behavior**: Hold gestures steady, avoid quick movements

## Technical Details

The application uses:
- **OpenCV** for camera input, image processing, and contour-based hand detection
- **Skin color detection** in HSV color space for hand tracking
- **Contour analysis** to classify hand gestures based on shape and finger count
- **pynput** for sending keyboard shortcuts (Space, J, L keys) to control YouTube
- **Gesture stabilization** to prevent erratic behavior

## Dependencies

- `opencv-python`: Camera input and computer vision
- `numpy`: Numerical operations for image processing
- `pynput`: Keyboard simulation for YouTube control