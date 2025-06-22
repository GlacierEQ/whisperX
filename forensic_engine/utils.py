"""
utils.py
Shared utility functions for the forensic engine pipeline.
"""
import os

def ensure_dir(path):
    """Ensure a directory exists."""
    os.makedirs(path, exist_ok=True)
