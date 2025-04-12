#!/usr/bin/env python3
import os
import sys
import platform
import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), "build_scripts"))

def ask_target_os():
    """Ask user for the target OS to build for and return the normalized value."""
    print("Which OS do you want to build for? Options: windows, darwin (macOS), linux")
    target_os = input("Enter target OS (press Enter to use current system): ").strip().lower()
    if not target_os:
        target_os = platform.system().lower()
    if target_os not in ['windows', 'darwin', 'linux']:
        print(f"Unsupported or unrecognized target OS: {target_os}")
        sys.exit(1)
    return target_os

def main():
    target_os = ask_target_os()
    if target_os == 'windows':
        from build_scripts.build_windows import build_windows
        build_windows()
    elif target_os == 'darwin':
        from build_scripts.build_macos import build_macos
        build_macos()
    elif target_os == 'linux':
        from build_scripts.build_linux import build_linux
        build_linux()
    else:
        print(f"Unsupported platform: {target_os}")
        sys.exit(1)

if __name__ == "__main__":
    main()
