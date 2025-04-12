import os
import re

def ensure_dir(directory):
    """Make sure a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_version():
    """Extract version from version file."""
    # Try to read from the version file
    if os.path.exists("version.txt"):
        with open("version.txt", "r") as f:
            return f.read().strip()

    # Default version if not found
    return "0.1.1"
