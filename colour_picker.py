"Recreating basic colour picker using python, featuring pyautogui and pynput."

import pyautogui
from pynput import keyboard

def find_mouse() -> tuple[int, int]:
    """Get current mouse position."""
    return pyautogui.position()

def find_rgb_val() -> tuple[int, int, tuple[int, int, int]]:
    """Get position and RGB color at current mouse location."""
    x, y = find_mouse()
    color = pyautogui.pixel(x, y)
    print(f"Position: ({x}, {y})")
    print(f"Color (RGB): {color}")
    return x, y, color

def wait(key):
    """Handle keyboard input to capture position and color."""
    try:
        if key == keyboard.Key.ctrl_l:
            find_rgb_val()
            return False
    except AttributeError:
        pass
    return True

if __name__ == "__main__":
    with keyboard.Listener(on_press=wait) as listener:
        listener.join()
