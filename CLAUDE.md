# YouTube Hand Gesture Control Project

## Overview
Python application that controls YouTube video playback using hand gestures detected via webcam.

## Gesture Mapping
- **Closed Hand (Fist)**: Pause video
- **Open Hand**: Resume playback  
- **Thumb Up**: Fast-forward 10 seconds
- **Little Finger Extended**: Rewind 10 seconds

## Technical Approach
- **Hand Detection**: MediaPipe for robust hand tracking
- **YouTube Control**: Keyboard shortcuts (spacebar, arrow keys)
- **Implementation**: Real-time gesture recognition with cooldown mechanism

## Dependencies
- opencv-python: Camera input and image processing
- mediapipe: Hand landmark detection
- pynput: Keyboard simulation for YouTube controls

## Key Features
- Works with any active YouTube tab
- Cooldown mechanism to prevent erratic behavior
- Real-time gesture feedback
- Robust against different lighting conditions