"""
intake_watcher.py
Watches the intake/ directory for new audio/video files and moves them to processing/ for batch processing.
"""

import os
import shutil
from time import sleep
from forensic_engine.meta.meta_tracker import log_action

INTAKE_DIR = "intake"
PROCESSING_DIR = "processing"
ALLOWED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".mp4",
    ".m4a",
    ".flac",
    ".aac",
    ".ogg",
    ".wma",
    ".avi",
    ".mov",
    ".mkv",
}


class IntakeWatcher:
    """Watch the intake directory and move files to processing."""

    def __init__(self, poll_interval: int = 10) -> None:
        """Initialize with the polling interval in seconds."""
        self.poll_interval = poll_interval

    def is_allowed_file(self, fname: str) -> bool:
        """Return True if *fname* has an allowed extension."""
        _, ext = os.path.splitext(fname)
        return ext.lower() in ALLOWED_EXTENSIONS

    def watch(self) -> None:  # pragma: no cover
        """Continuously watch intake/ and move new files to processing/."""
        while True:
            for fname in os.listdir(INTAKE_DIR):
                fpath = os.path.join(INTAKE_DIR, fname)
                if os.path.isfile(fpath) and self.is_allowed_file(fname):
                    dest = os.path.join(PROCESSING_DIR, fname)
                    shutil.move(fpath, dest)
                    log_action(
                        "intake_move",
                        {"file": fname, "from": INTAKE_DIR, "to": PROCESSING_DIR},
                    )
            sleep(self.poll_interval)


if __name__ == "__main__":  # pragma: no cover
    os.makedirs(INTAKE_DIR, exist_ok=True)
    os.makedirs(PROCESSING_DIR, exist_ok=True)
    watcher = IntakeWatcher()
    watcher.watch()
