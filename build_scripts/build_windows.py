#!/usr/bin/env python3
import os
import shutil
import subprocess
from common import ensure_dir, get_version

def build_windows():
    # Clean previous builds
    print("Cleaning previous builds...")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # Create Windows executable
    print("Building Windows executable...")
    subprocess.run([
        "pyinstaller",
        "--name=HashtagGenerator",
        "--windowed",
        "--onefile",
        "--noconsole",
        "--icon=assets/icons/app_icon.ico",
        "--add-data=assets;assets",
        "src/gui/main.py"
    ], check=True)
    
    # Add version info and metadata (requires pyinstaller-versionfile)
    version = get_version()
    subprocess.run([
        "python", "-m", "pyinstaller_versionfile",
        "--version-file-version", version,
        "--file-description", "A Hashtag Generator",
        "--product-name", "Hashtag Generator",
        "--company-name", "Hashtag Generator Project",
        "--version-file", "version.txt"
    ], check=True)
    
    # Rebuild with version info
    subprocess.run([
        "pyinstaller",
        "--name=HashtagGenerator",
        "--onefile",
        "--windowed",
        "--icon=assets/icons/app_icon.ico",
        "--add-data=assets;assets",
        "--version-file=version.txt",
        "src/gui/main.py"
    ], check=True)
    
    print("Windows build completed successfully!")

if __name__ == "__main__":
    build_windows()
