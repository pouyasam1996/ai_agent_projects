from pynput import keyboard
import time

def start_keyboard_listener():
    def on_press(key):
        try:
            if keyboard.Key.shift in pressed:
                if key == keyboard.Key.up:
                    with open("scroll.txt", "w") as f:
                        f.write("up")
                elif key == keyboard.Key.down:
                    with open("scroll.txt", "w") as f:
                        f.write("down")
                elif key == keyboard.Key.left:
                    with open("scroll.txt", "w") as f:
                        f.write("left")
                elif key == keyboard.Key.right:
                    with open("scroll.txt", "w") as f:
                        f.write("right")
        except Exception as e:
            print(f"Error: {e}")

    pressed = set()
    listener = keyboard.Listener(on_press=on_press)
    listener.start()