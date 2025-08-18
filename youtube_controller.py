from pynput.keyboard import Key, Controller
import time

class YouTubeController:
    def __init__(self):
        self.keyboard = Controller()
        self.last_action_time = 0
        self.cooldown_period = 1.0  # 1 second cooldown between actions
    
    def can_perform_action(self) -> bool:
        current_time = time.time()
        if current_time - self.last_action_time >= self.cooldown_period:
            self.last_action_time = current_time
            return True
        return False
    
    def pause_video(self):
        if self.can_perform_action():
            self.keyboard.press(Key.space)
            self.keyboard.release(Key.space)
            print("Action: Paused video")
    
    def play_video(self):
        if self.can_perform_action():
            self.keyboard.press(Key.space)
            self.keyboard.release(Key.space)
            print("Action: Resumed video")
    
    def fast_forward(self, seconds: int = 10):
        if self.can_perform_action():
            # YouTube shortcut: Right arrow for 5 seconds, 'l' for 10 seconds
            self.keyboard.press('l')
            self.keyboard.release('l')
            print(f"Action: Fast-forwarded {seconds} seconds")
    
    def rewind(self, seconds: int = 10):
        if self.can_perform_action():
            # YouTube shortcut: Left arrow for 5 seconds, 'j' for 10 seconds
            self.keyboard.press('j')
            self.keyboard.release('j')
            print(f"Action: Rewound {seconds} seconds")
    
    def set_cooldown(self, seconds: float):
        self.cooldown_period = seconds