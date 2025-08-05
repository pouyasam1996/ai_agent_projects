#!/usr/bin/env python3
"""
Universal startup script for AI Interview Assistant
Works on Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import platform


def main():
    # Get the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    scripts_dir = os.path.join(project_root, "scripts")
    main_script = os.path.join(scripts_dir, "main.py")

    print(f"🚀 Starting AI Interview Assistant from: {project_root}")
    print(f"🐍 Python version: {sys.version}")
    print(f"💻 Platform: {platform.system()}")

    # Check if main script exists
    if not os.path.exists(main_script):
        print(f"❌ Error: {main_script} not found!")
        return 1

    # Run the main script
    try:
        subprocess.run([sys.executable, main_script], cwd=scripts_dir)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        return 0
    except Exception as e:
        print(f"❌ Error running application: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())