"""
case_router.py
Moves processed files from processing/ to the correct case folder in cases/.
Auto-creates case folders and organizes by type (audio, transcripts, spectral, analysis).
"""

import os
import shutil

from forensic_engine.utils import validate_case_id
from forensic_engine.case_builder import sanitize_filename


CASES_DIR = "cases"


class CaseRouter:
    """Route processed files to case folders."""

    def __init__(self) -> None:
        """Initialize the case router."""
        pass

    def route_file(self, fname: str, case_id: str, file_type: str) -> None:
        """Move file to /cases/{case_id}/{file_type}/, auto-create folders."""
        validate_case_id(case_id)
        dest_dir = os.path.join(CASES_DIR, case_id, file_type)
        os.makedirs(dest_dir, exist_ok=True)

        sanitized_basename = sanitize_filename(os.path.basename(fname))
        dest = os.path.join(dest_dir, sanitized_basename)

        shutil.move(fname, dest)

    def route_batch(self, files: list[str], case_id_map: dict) -> None:
        """Route a batch of files using a mapping of filename to (case_id, file_type)."""
        for fname in files:
            case_id, file_type = case_id_map.get(fname, ("unknown_case", "misc"))
            self.route_file(fname, case_id, file_type)


if __name__ == "__main__":
    os.makedirs(CASES_DIR, exist_ok=True)
