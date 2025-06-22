"""
case_router.py
Moves processed files from processing/ to the correct case folder in cases/.
Auto-creates case folders and organizes by type (audio, transcripts, spectral, analysis).
"""
import os
import shutil

CASES_DIR = 'cases'

class CaseRouter:
    def __init__(self):
        pass

    def route_file(self, fname, case_id, file_type):
        """Move file to /cases/{case_id}/{file_type}/, auto-create folders."""
        dest_dir = os.path.join(CASES_DIR, case_id, file_type)
        os.makedirs(dest_dir, exist_ok=True)
        shutil.move(fname, os.path.join(dest_dir, os.path.basename(fname)))
        print(f"Moved {fname} to {dest_dir}")

    def route_batch(self, files, case_id_map):
        """Route a batch of files using a mapping of filename to (case_id, file_type)."""
        for fname in files:
            case_id, file_type = case_id_map.get(fname, ("unknown_case", "misc"))
            self.route_file(fname, case_id, file_type)

if __name__ == "__main__":
    os.makedirs(CASES_DIR, exist_ok=True)
    # Example usage:
    # router = CaseRouter()
    # router.route_file('example.wav', 'case_001', 'audio')
