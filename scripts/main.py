import os
import sys
from pynput import keyboard
import pyautogui
import time
from web_server import start_server
import subprocess
import webbrowser

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "screenshots")


def capture_screenshot():
    pressed = set()
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    screenshot_path = os.path.join(SCREENSHOTS_DIR, "screenshot.png")

    def on_press(key):
        try:
            pressed.add(key)
            if (keyboard.Key.cmd in pressed and
                    keyboard.Key.shift in pressed and
                    keyboard.KeyCode.from_char('7') in pressed):
                screenshot = pyautogui.screenshot()
                screenshot.save(screenshot_path)
                if os.path.exists(screenshot_path):
                    print(f"📸 Screenshot saved: {screenshot_path}")
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
        print("🐍 Press Ctrl+Shift+P for Python or ⚡ Ctrl+Shift+C for C++...")
        choice_made = [False]

        def on_choice_press(key):
            try:
                pressed.add(key)
                if (keyboard.Key.ctrl in pressed and
                        keyboard.Key.shift in pressed):
                    if keyboard.KeyCode.from_char('c') in pressed:
                        print("⚡ Running C++ analysis...")
                        script_path = os.path.join(os.path.dirname(__file__), "ai_agent_cpp_gpt.py")
                        subprocess.run([sys.executable, script_path, screenshot_path])
                        print_result_link()
                        choice_made[0] = True
                        return False
                    elif keyboard.KeyCode.from_char('p') in pressed:
                        print("🐍 Running Python analysis...")
                        script_path = os.path.join(os.path.dirname(__file__), "ai_agent_python_gpt.py")
                        subprocess.run([sys.executable, script_path, screenshot_path])
                        print_result_link()
                        choice_made[0] = True
                        return False
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

        return False

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def print_result_link():
    """Print clickable link and optionally open browser"""
    url = "http://localhost:5001"
    print("\n" + "=" * 60)
    print("🎉 AI Analysis Complete!")
    print("=" * 60)
    print(f"📄 Results are ready! View at: {url}")
    print("=" * 60)
    print("Press 'o' + Enter to open in browser, or just visit the link above")
    print("=" * 60 + "\n")


def main():
    print("🚀 Starting AI Interview Assistant...")

    # Ensure we're in the scripts directory for relative imports
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(scripts_dir)

    # Start web server
    start_server()
    time.sleep(2)  # Give server time to start

    url = "http://localhost:5001"
    print("\n" + "=" * 60)
    print("🤖 AI Interview Assistant Ready!")
    print("=" * 60)
    print(f"📱 Web Interface: {url}")
    print("⌨️  Capture Screenshot: Cmd+Shift+7")
    print("🐍 Python Solutions: Ctrl+Shift+P")
    print("⚡ C++ Solutions: Ctrl+Shift+C")
    print(f"📁 Project Directory: {PROJECT_ROOT}")
    print("=" * 60 + "\n")

    while True:
        capture_screenshot()
        time.sleep(1)


if __name__ == "__main__":
    main()