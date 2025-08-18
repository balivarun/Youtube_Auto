import cv2
import numpy as np
from typing import Optional

class SimpleHandGestureDetector:
    """
    Simple hand gesture detector using OpenCV without MediaPipe
    Uses contour detection and basic shape analysis
    """
    
    def __init__(self):
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
        self.gesture_stable_count = 0
        self.gesture_threshold = 3  # Need 3 consecutive frames for stability
        self.last_gesture = None
        
    def detect_gesture(self, frame) -> Optional[str]:
        """Detect hand gesture from frame using contour analysis"""
        try:
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Define range for skin color (adjust as needed)
            lower_skin = np.array([0, 20, 70], dtype=np.uint8)
            upper_skin = np.array([20, 255, 255], dtype=np.uint8)
            
            # Create mask for skin color
            mask = cv2.inRange(hsv, lower_skin, upper_skin)
            
            # Apply morphological operations to clean up the mask
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Apply Gaussian blur
            mask = cv2.GaussianBlur(mask, (5, 5), 0)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return self._stabilize_gesture(None)
            
            # Find the largest contour (assumed to be the hand)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Filter out small contours
            if cv2.contourArea(largest_contour) < 5000:
                return self._stabilize_gesture(None)
            
            # Analyze the contour to determine gesture
            gesture = self._analyze_contour(largest_contour)
            return self._stabilize_gesture(gesture)
            
        except Exception as e:
            print(f"Error in gesture detection: {e}")
            return None
    
    def _analyze_contour(self, contour) -> str:
        """Analyze contour shape to determine gesture"""
        try:
            # Calculate contour properties
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            
            if perimeter == 0:
                return "unknown"
            
            # Calculate circularity
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            
            # Find convex hull and convexity defects
            hull = cv2.convexHull(contour, returnPoints=False)
            
            if len(hull) > 3:
                defects = cv2.convexityDefects(contour, hull)
                
                if defects is not None:
                    # Count significant defects (fingers)
                    finger_count = 0
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        
                        # Calculate distance from defect point to hull
                        if d > 10000:  # Adjust threshold as needed
                            finger_count += 1
                    
                    # Simple gesture classification based on finger count and shape
                    if finger_count == 0 and circularity > 0.7:
                        return "fist"
                    elif finger_count >= 4:
                        return "open_hand"
                    elif finger_count == 1:
                        # Could be thumb up or pinky - use position analysis
                        return self._analyze_finger_position(contour)
                    else:
                        return "unknown"
            
            # Fallback: use circularity alone
            if circularity > 0.7:
                return "fist"
            else:
                return "open_hand"
                
        except Exception as e:
            print(f"Error analyzing contour: {e}")
            return "unknown"
    
    def _analyze_finger_position(self, contour) -> str:
        """Analyze finger position for thumb_up vs pinky_up detection"""
        try:
            # Find the topmost and bottommost points
            topmost = tuple(contour[contour[:, :, 1].argmin()][0])
            bottommost = tuple(contour[contour[:, :, 1].argmax()][0])
            leftmost = tuple(contour[contour[:, :, 0].argmin()][0])
            rightmost = tuple(contour[contour[:, :, 0].argmax()][0])
            
            # Simple heuristic: if the finger is on the right side, assume thumb_up
            # if on the left side, assume pinky_up
            center_x = (leftmost[0] + rightmost[0]) // 2
            
            if rightmost[0] > center_x + (rightmost[0] - leftmost[0]) * 0.3:
                return "thumb_up"
            elif leftmost[0] < center_x - (rightmost[0] - leftmost[0]) * 0.3:
                return "pinky_up"
            else:
                return "thumb_up"  # Default to thumb_up
                
        except Exception:
            return "thumb_up"  # Default fallback
    
    def _stabilize_gesture(self, gesture: str) -> Optional[str]:
        """Stabilize gesture detection to avoid flickering"""
        if gesture == self.last_gesture:
            self.gesture_stable_count += 1
        else:
            self.gesture_stable_count = 1
            self.last_gesture = gesture
        
        # Only return gesture if it's been stable for enough frames
        if self.gesture_stable_count >= self.gesture_threshold:
            return gesture
        
        return None