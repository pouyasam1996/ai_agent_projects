import pyautogui
import keyboard
import time
import os

def capture_screenshot():
    # Wait for Cmd+Shift+7
    if keyboard.is_pressed("cmd+shift+7"):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"screenshot_{timestamp}.png"
        pyautogui.screenshot(screenshot_path)
        return screenshot_path
    return None