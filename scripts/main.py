# /Users/pouyasamandi/Desktop/Agent_projects/interview_ai/scripts/main.py
from pynput import keyboard
import pyautogui
import os
import time
from web_server import start_server
import subprocess

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
                    # Wait for Ctrl+Shift+C or Ctrl+Shift+P
                    return wait_for_choice(screenshot_path)
        except Exception as e:
            print(f"Error: {e}")
        return True

    def on_release(key):
        try:
            pressed.discard(key)
        except Exception:
            pass

    def wait_for_choice(screenshot_path):
        print("Press Ctrl+Shift+C for C++ or Ctrl+Shift+P for Python...")
        choice_made = [False]  # Mutable flag to track choice

        def on_choice_press(key):
            try:
                pressed.add(key)
                if (keyboard.Key.ctrl in pressed and
                    keyboard.Key.shift in pressed):
                    if keyboard.KeyCode.from_char('c') in pressed:
                        print("Running ai_agent_cpp.py...")
                        subprocess.run(["python", "ai_agent_cpp.py", screenshot_path])
                        choice_made[0] = True
                        return False  # Stop listener
                    elif keyboard.KeyCode.from_char('p') in pressed:
                        print("Running ai_agent_python_gpt.py...")
                        subprocess.run(["python", "ai_agent_python_gpt.py", screenshot_path])
                        choice_made[0] = True
                        return False  # Stop listener
            except Exception as e:
                print(f"Choice error: {e}")
            return True

        def on_choice_release(key):
            try:
                pressed.discard(key)
            except Exception:
                pass

        with keyboard.Listener(on_press=on_choice_press, on_release=on_choice_release) as choice_listener:
            choice_listener.join()

        return False  # Stop main listener after choice

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