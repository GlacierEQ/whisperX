"""
utils.py
Shared utility functions for the forensic engine pipeline.
"""

import os


def ensure_dir(path: str) -> None:
    """Ensure a directory exists."""
    os.makedirs(path, exist_ok=True)


def validate_case_id(case_id: str) -> None:
    """Raise :class:`ValueError` if *case_id* contains invalid characters."""
    if not case_id or any(ch for ch in case_id if not (ch.isalnum() or ch == "_")):
        raise ValueError(f"invalid case_id: {case_id}")
