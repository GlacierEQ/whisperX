"""case_router.py

Move processed files from ``processing/`` to the appropriate case folder under
``cases/``. Destination folders are created automatically and organized by file
type (audio, transcripts, spectral, analysis).
"""

import os
import shutil
from .utils import ensure_dir
from .case_builder import sanitize_filename

CASES_DIR = "cases"


class CaseRouter:
    def __init__(self):
        pass

    def route_file(self, fname, case_id, file_type):
        """Move file to /cases/{case_id}/{file_type}/ using a sanitized name."""
        dest_dir = os.path.join(CASES_DIR, case_id, file_type)
        ensure_dir(dest_dir)
        dest = os.path.join(dest_dir, sanitize_filename(os.path.basename(fname)))
        shutil.move(fname, dest)
        print(f"Moved {fname} to {dest_dir}")

    def route_batch(self, files, case_id_map):
        """Route a batch of files using a ``filename -> (case_id, file_type)`` map."""
        for fname in files:
            case_id, file_type = case_id_map.get(fname, ("unknown_case", "misc"))
            self.route_file(fname, case_id, file_type)


if __name__ == "__main__":
    os.makedirs(CASES_DIR, exist_ok=True)
