#!/usr/bin/env python3
import os
import sys
import platform
import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), "build_scripts"))

def install_pyinstaller():
    """Install PyInstaller using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller-versionfile"])
        print("PyInstaller installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install PyInstaller: {e}")
def main():
    system = platform.system().lower()

    if system == 'windows':
        from build_scripts.build_windows import build_windows
        build_windows()
    elif system == 'darwin':
        from build_scripts.build_macos import build_macos
        build_macos()
    elif system == 'linux':
        from build_scripts.build_linux import build_linux
        build_linux()
    else:
        print(f"Unsupported platform: {system}")
        sys.exit(1)

if __name__ == "__main__":
    install_pyinstaller()
    main()
