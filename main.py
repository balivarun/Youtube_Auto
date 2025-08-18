import cv2
import time
from simple_gesture_detector import SimpleHandGestureDetector
from youtube_controller import YouTubeController

class YouTubeGestureControl:
    def __init__(self):
        self.gesture_detector = SimpleHandGestureDetector()
        self.youtube_controller = YouTubeController()
        self.cap = None
        self.current_gesture = None
        self.previous_gesture = None
        self.gesture_start_time = 0
        self.gesture_hold_threshold = 1.0  # Hold gesture for 1 second
        
    def initialize_camera(self, camera_index: int = 0) -> bool:
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            print("Error: Could not open camera")
            return False
        
        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("Camera initialized successfully")
        return True
    
    def process_gesture(self, gesture: str):
        current_time = time.time()
        
        # Check if gesture changed
        if gesture != self.previous_gesture:
            self.current_gesture = gesture
            self.gesture_start_time = current_time
            self.previous_gesture = gesture
            return
        
        # Check if gesture has been held long enough
        if (self.current_gesture == gesture and 
            current_time - self.gesture_start_time >= self.gesture_hold_threshold):
            
            # Execute action based on gesture
            if gesture == "fist":
                self.youtube_controller.pause_video()
            elif gesture == "open_hand":
                self.youtube_controller.play_video()
            elif gesture == "thumb_up":
                self.youtube_controller.fast_forward()
            elif gesture == "pinky_up":
                self.youtube_controller.rewind()
            
            # Reset to prevent repeated actions
            self.gesture_start_time = current_time + self.youtube_controller.cooldown_period
    
    def run(self):
        if not self.initialize_camera():
            return
        
        print("YouTube Gesture Control Started!")
        print("IMPORTANT: Make sure your YouTube tab is active/focused!")
        print("\nGestures:")
        print("- Fist (closed hand): Pause/Play")
        print("- Open Hand (all fingers extended): Play/Pause")
        print("- Thumb Up: Fast Forward 10s")
        print("- Pinky Up: Rewind 10s")
        print("\nTips:")
        print("- Keep your hand steady for 1 second")
        print("- Use good lighting")
        print("- Position hand against contrasting background")
        print("\nPress 'q' to quit")
        
        # Give user time to position themselves
        print("\nStarting in 3 seconds...")
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Could not read frame")
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Detect gesture
                gesture = self.gesture_detector.detect_gesture(frame)
                
                # Process gesture if detected
                if gesture and gesture != "unknown":
                    self.process_gesture(gesture)
                
                # Display current gesture on frame
                if gesture:
                    cv2.putText(frame, f"Gesture: {gesture}", (10, 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "No gesture detected", (10, 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                # Show instructions
                instructions = [
                    "Fist: Pause | Open: Play",
                    "Thumb Up: +10s | Pinky Up: -10s",
                    "Press 'q' to quit"
                ]
                
                for i, instruction in enumerate(instructions):
                    y_pos = frame.shape[0] - 60 + (i * 20)
                    cv2.putText(frame, instruction, (10, y_pos), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # Display frame
                cv2.imshow('YouTube Gesture Control', frame)
                
                # Check for quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            self.cleanup()
    
    def cleanup(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Cleanup completed")

if __name__ == "__main__":
    app = YouTubeGestureControl()
    app.run()