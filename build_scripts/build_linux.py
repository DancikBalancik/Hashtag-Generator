#!/usr/bin/env python3
import os
import shutil
import subprocess
from common import ensure_dir, get_version

def build_linux():
    # Clean previous builds
    print("Cleaning previous builds...")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # Create Linux executable
    print("Building Linux executable...")
    subprocess.run([
        "pyinstaller",
        "--name=hashtag-generator",
        "--windowed",
        "--icon=assets/icons/app_icon.png",
        "--add-data=assets:assets",
        "src\gui\main.py"
    ], check=True)
    
    # Create .desktop file for Linux application menus
    version = get_version()
    desktop_file = f"""[Desktop Entry]
Name=Hashtag Generator
Comment=Transform text into hashtag format
Exec=hashtag-generator
Icon=/usr/share/icons/hicolor/256x256/apps/hashtag-generator.png
Terminal=false
Type=Application
Categories=Utility;TextTools;
Keywords=hashtag;social;text;
Version={version}
"""
    
    os.makedirs("dist/linux", exist_ok=True)
    with open("dist/linux/hashtag-generator.desktop", "w") as f:
        f.write(desktop_file)
    
    # Copy icon for system installation
    icons_dir = "dist/linux/icons/hicolor/256x256/apps"
    os.makedirs(icons_dir, exist_ok=True)
    shutil.copy("assets/icons/app_icon.png", f"{icons_dir}/hashtag-generator.png")
    
    # Create AppImage (optional, requires appimagetool)
    try:
        print("Creating AppImage...")
        # Create AppDir structure
        appdir = "dist/AppDir"
        ensure_dir(appdir)
        shutil.copy("dist/hashtag-generator", f"{appdir}/AppRun")
        os.chmod(f"{appdir}/AppRun", 0o755)  # Make executable
        shutil.copy("dist/linux/hashtag-generator.desktop", f"{appdir}/hashtag-generator.desktop")
        shutil.copy("--icon=assets/icons/app_icon.png", f"{appdir}/.DirIcon")
        
        # Create icons directory in AppDir
        icons_appdir = f"{appdir}/usr/share/icons/hicolor/256x256/apps"
        os.makedirs(icons_appdir, exist_ok=True)
        shutil.copy("--icon=assets/icons/app_icon.png", f"{icons_appdir}/hashtag-generator.png")
        
        # Run appimagetool
        subprocess.run([
            "appimagetool",
            appdir,
            f"dist/HashtagGenerator-{version}-x86_64.AppImage"
        ], check=True)
        print("AppImage created successfully!")
    except Exception as e:
        print(f"AppImage creation failed: {e}")
        print("You can install appimagetool to create AppImages")
    
    print("Linux build completed successfully!")

if __name__ == "__main__":
    build_linux()
