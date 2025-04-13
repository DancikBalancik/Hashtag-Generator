#!/usr/bin/env python3
import os
import shutil
import subprocess
import plistlib
from common import ensure_dir, get_version

def build_macos():
    # Clean previous builds
    print("Cleaning previous builds...")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # Create macOS app bundle
    print("Building macOS application...")
    subprocess.run([
        "pyinstaller",
        "--name=HashtagGenerator",
        "--windowed",
        "--onefile",
        "--noconsole",
        "--icon=assets/icons/app_icon.icns",
        "--add-data=assets:assets",
        "--osx-bundle-identifier=com.hashtaggenerator.app",
        "src/gui/main.py"
    ], check=True)
    
    # Update Info.plist with additional metadata
    version = get_version()
    info_plist_path = "dist/HashtagGenerator.app/Contents/Info.plist"
    
    with open(info_plist_path, 'rb') as f:
        info_plist = plistlib.load(f)
    
    # Update with app-specific information
    info_plist.update({
        'CFBundleShortVersionString': version,
        'CFBundleVersion': version,
        'NSHumanReadableCopyright': f'© {2025} Hashtag Generator Project',
        'LSApplicationCategoryType': 'public.app-category.utilities',
    })
    
    with open(info_plist_path, 'wb') as f:
        plistlib.dump(info_plist, f)
    
    print("macOS build completed successfully!")
    
    # Optional: Create DMG file (requires create-dmg)
    try:
        print("Creating DMG installer...")
        subprocess.run([
            "create-dmg",
            "--volname", "Hashtag Generator",
            "--volicon", "assets/icons/app_icon.icns",
            "--window-pos", "200", "100",
            "--window-size", "800", "400",
            "--icon-size", "100",
            "--icon", "HashtagGenerator.app", "200", "190",
            "--hide-extension", "HashtagGenerator.app",
            "--app-drop-link", "600", "190",
            f"dist/HashtagGenerator-{version}.dmg",
            "dist/HashtagGenerator.app"
        ], check=True)
        print("DMG created successfully!")
    except Exception as e:
        print(f"DMG creation failed: {e}")
        print("You can manually create a DMG using Disk Utility or install create-dmg")

if __name__ == "__main__":
    build_macos()
