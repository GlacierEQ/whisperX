"""case_builder.py

Provide utilities for organizing case folders and sanitizing filenames.
"""

import os
import re
import shutil
from .utils import ensure_dir
from .config import CASES_DIR


FILENAME_SAFE_PATTERN = re.compile(r"[^A-Za-z0-9._-]")


def sanitize_filename(name):
    """Return a filesystem-safe version of ``name``."""
    return FILENAME_SAFE_PATTERN.sub("_", name)


def parse_case_id(fname: str) -> str | None:
    """Return the case identifier parsed from *fname*."""
    parts = fname.split("_")
    for i, part in enumerate(parts):
        if part == "case" and i + 1 < len(parts):
            return f"case_{os.path.splitext(parts[i + 1])[0]}"
        if part.startswith("case") and any(ch.isdigit() for ch in part[4:]):
            return os.path.splitext(part)[0]
    return None


class CaseBuilder:
    """Manage creation and population of case directories."""

    def __init__(self, base_dir=CASES_DIR):
        self.base_dir = base_dir

    def create_structure(self, case_id):
        """Create standard subfolders for ``case_id``."""
        for sub in ["audio", "transcripts", "spectral", "analysis"]:
            ensure_dir(os.path.join(self.base_dir, case_id, sub))

    def add_file(self, src, case_id, file_type):
        """Move ``src`` into the case folder using a sanitized name."""
        self.create_structure(case_id)
        dest_name = sanitize_filename(os.path.basename(src))
        dest = os.path.join(self.base_dir, case_id, file_type, dest_name)
        shutil.move(src, dest)
        return dest
