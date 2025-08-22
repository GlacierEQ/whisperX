"""
batch_processor.py
Processes files in processing/ in batches (default: 3 at a time).
Runs WhisperX transcription, diarization, spectral imaging, and renaming.
Creates a per-file folder in the appropriate case directory.
Handles errors, logs all actions, and supports configuration.
"""

import os
import re
from concurrent.futures import ThreadPoolExecutor
import shutil
from time import sleep
from forensic_engine.meta.meta_tracker import log_action
from forensic_engine.config import (
    PROCESSING_DIR,
    PROCESSED_DIR,
    CASES_DIR,
    QUARANTINE_DIR,
    BATCH_SIZE,
    NUM_WORKERS,
    POLL_INTERVAL,
    ALLOWED_EXTENSIONS,
)
from forensic_engine.case_builder import sanitize_filename
from forensic_engine.utils import ensure_dir, validate_case_id

# TODO: Import actual WhisperX, pyannote, and spectral imaging modules


CASE_ID_PATTERN = re.compile(r"case_?\d+")


def get_case_id(fname: str) -> str | None:
    """Extract the ``case_<id>`` portion from a filename."""
    match = CASE_ID_PATTERN.search(fname)
    return match.group(0) if match else None


def process_file(fname: str) -> None:
    """Process a single file from the processing queue."""
    try:
        case_id = get_case_id(fname)
        if not case_id:
            ensure_dir(QUARANTINE_DIR)
            shutil.move(
                os.path.join(PROCESSING_DIR, fname), os.path.join(QUARANTINE_DIR, fname)
            )
            log_action("quarantine", {"file": fname, "reason": "no_case_id"})
            return

        validate_case_id(case_id)  # from integration branch

        file_id = os.path.splitext(sanitize_filename(fname))[0]
        file_folder = os.path.join(CASES_DIR, case_id, "audio", file_id)
        ensure_dir(file_folder)

        src = os.path.join(PROCESSING_DIR, fname)
        dest = os.path.join(
            file_folder, "original" + os.path.splitext(sanitize_filename(fname))[1]
        )
        shutil.move(src, dest)
        log_action("file_routed", {"file": fname, "to": file_folder})

        # --- WhisperX transcription ---
        transcript_path = os.path.join(file_folder, "transcript.txt")
        with open(transcript_path, "w") as f:
            f.write(f"[Stub transcript for {fname}]")
        log_action("transcription", {"file": fname, "output": transcript_path})

        # --- Diarization ---
        diarization_path = os.path.join(file_folder, "diarization.json")
        with open(diarization_path, "w") as f:
            f.write(f"{{'stub': 'diarization for {fname}'}}")
        log_action("diarization", {"file": fname, "output": diarization_path})

        # --- Spectral Imaging ---
        spectrogram_path = os.path.join(file_folder, "spectrogram.png")
        with open(spectrogram_path, "wb") as f:
            f.write(b"")  # Placeholder for image
        log_action("spectrogram", {"file": fname, "output": spectrogram_path})

        # Move to processed
        ensure_dir(PROCESSED_DIR)
        shutil.copy(dest, os.path.join(PROCESSED_DIR, sanitize_filename(fname)))
    except Exception as e:
        log_action("batch_error", {"file": fname, "error": str(e)})


def process_batch(files: list[str]) -> None:
    """Process a list of files concurrently."""
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as exc:
        list(exc.map(process_file, files))


def run_batch_processor() -> None:  # pragma: no cover
    """Continuously process files from the processing queue."""
    ensure_dir(PROCESSING_DIR)
    ensure_dir(PROCESSED_DIR)
    ensure_dir(CASES_DIR)
    ensure_dir(QUARANTINE_DIR)
    while True:
        files = [
            f
            for f in os.listdir(PROCESSING_DIR)
            if os.path.isfile(os.path.join(PROCESSING_DIR, f))
            and os.path.splitext(f)[1].lower() in ALLOWED_EXTENSIONS
        ]
        if len(files) >= BATCH_SIZE:
            batch = files[:BATCH_SIZE]
            log_action("batch_start", {"files": batch})
            process_batch(batch)
            log_action("batch_end", {"files": batch})
        else:
            sleep(POLL_INTERVAL)


if __name__ == "__main__":  # pragma: no cover
    run_batch_processor()
