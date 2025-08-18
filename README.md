# YouTube Hand Gesture Control

Control YouTube video playback using hand gestures detected through your webcam.

## Features

- **Fist**: Pause video
- **Open Hand**: Resume playback
- **Thumbs Up**: Fast-forward 10 seconds
- **Pinky Up**: Rewind 10 seconds

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

## Usage

1. Open YouTube in your browser
2. Start playing a video
3. Run the Python application
4. Position your hand in front of the webcam
5. Make gestures to control playback
6. Press 'q' in the camera window to quit

## Requirements

- Python 3.7+
- Webcam
- Active YouTube tab in browser

## Troubleshooting

- Ensure your webcam is working and not being used by other applications
- Make sure the YouTube tab is active for keyboard shortcuts to work
- Adjust lighting for better hand detection
- Keep your hand steady for gesture recognition

## Technical Details

The application uses:
- **MediaPipe** for hand landmark detection
- **OpenCV** for camera input and image processing
- **pynput** for sending keyboard shortcuts to control YouTube