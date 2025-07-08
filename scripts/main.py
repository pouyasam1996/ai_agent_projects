# /Users/pouyasamandi/Desktop/Agent_projects/interview_ai/scripts/main.py
from pynput import keyboard
import pyautogui
import os
import time
from ai_agent import process_screenshot
from web_server import start_server

def capture_screenshot():
    pressed = set()
    save_dir = "/Users/pouyasamandi/Desktop/Agent_projects/interview_ai/screenshots"
    os.makedirs(save_dir, exist_ok=True)
    screenshot_path = os.path.join(save_dir, "screenshot.png")

    def on_press(key):
        try:
            pressed.add(key)
            if (keyboard.Key.cmd in pressed and
                keyboard.Key.shift in pressed and
                keyboard.KeyCode.from_char('7') in pressed):
                screenshot = pyautogui.screenshot()
                screenshot.save(screenshot_path)
                if os.path.exists(screenshot_path):
                    print(f"Screenshot saved: {screenshot_path}")
                    # Call AI agent
                    result = process_screenshot(screenshot_path)
                    print("AI Result:", result)
                    # Save result to file
                    with open("/Users/pouyasamandi/Desktop/Agent_projects/interview_ai/results.txt", "w") as f:
                        f.write(result)
                return False  # Stop listener after capture
        except Exception as e:
            print(f"Error: {e}")
        return True

    def on_release(key):
        try:
            pressed.discard(key)
        except Exception:
            pass

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    # Start web server
    start_server()
    print("Press Cmd+Shift+7 to capture screenshot...")
    while True:
        capture_screenshot()
        time.sleep(1)

if __name__ == "__main__":
    main()