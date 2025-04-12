import os
import re

def ensure_dir(directory):
    """Make sure a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_version():
    """Extract version from source code or version file."""
    # Try to read from a version file first
    if os.path.exists("version.txt"):
        with open("version.txt", "r") as f:
            return f.read().strip()

    # Alternatively, extract from source code
    with open("src\gui\main.py", "r") as f:
        content = f.read()
        match = re.search(r'VERSION\s*=\s*[\'"](.+?)[\'"]', content)
        if match:
            return match.group(1)

    # Default version if not found
    return "0.1.0"
