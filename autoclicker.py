'''Educational experiments into automating mouse clicks and keyboard inputs using Python.'''

import pyautogui
import time
import threading

from pynput import keyboard
class Clicker:
    """Handles automated mouse clicking with keyboard control."""
    def __init__(self, interval=0.1):
        self.interval = interval
        self.running = False

    def clicker(self):
        """Click the mouse repeatedly while running is True."""
        while True:
            if self.running:
                print("Clicking...")
                pyautogui.leftClick()
                time.sleep(0.05)
            else:
                time.sleep(0.1)  # Sleep briefly when not running to avoid busy waiting

    def on_press(self, key):
        """Handle keyboard input to control clicker and exit."""
        try:
            if key == keyboard.Key.esc:
                print("Exiting clicker...")
                return False  # Stop listener
            if key == keyboard.Key.ctrl_l:
                self.running = not self.running
                print(f"Clicker {'started' if self.running else 'stopped'}.")
        except AttributeError:
            pass  # Ignore unknown keys
        return True


clicker_obj = Clicker(interval=0.1)

worker = threading.Thread(target=clicker_obj.clicker, daemon=True)
worker.start()

with keyboard.Listener(on_press=clicker_obj.on_press) as listener:
    listener.join()
