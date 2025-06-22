"""
batch_processor.py
Processes files in processing/ in batches (default: 3 at a time).
Runs WhisperX transcription, diarization, spectral imaging, and renaming.
Creates a per-file folder in the appropriate case directory.
Handles errors, logs all actions, and supports configuration.
"""
import os
import shutil
from time import sleep
from meta.meta_tracker import log_action
from config import PROCESSING_DIR, PROCESSED_DIR, CASES_DIR, QUARANTINE_DIR, BATCH_SIZE, POLL_INTERVAL, ALLOWED_EXTENSIONS

# TODO: Import actual WhisperX, pyannote, and spectral imaging modules

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def get_case_id(fname):
    # TODO: Extract case_id from filename or metadata
    # Example: 'case_001_audio_1234.wav' -> 'case_001'
    parts = fname.split('_')
    for part in parts:
        if part.startswith('case'):
            return part
    return None

def process_file(fname):
    try:
        case_id = get_case_id(fname)
        if not case_id:
            # Move to quarantine and log
            ensure_dir(QUARANTINE_DIR)
            shutil.move(os.path.join(PROCESSING_DIR, fname), os.path.join(QUARANTINE_DIR, fname))
            log_action('quarantine', {'file': fname, 'reason': 'no_case_id'})
            return
        # Create per-file folder
        file_id = os.path.splitext(fname)[0]
        file_folder = os.path.join(CASES_DIR, case_id, 'audio', file_id)
        ensure_dir(file_folder)
        # Move original file
        src = os.path.join(PROCESSING_DIR, fname)
        dest = os.path.join(file_folder, 'original' + os.path.splitext(fname)[1])
        shutil.move(src, dest)
        log_action('file_routed', {'file': fname, 'to': file_folder})
        # --- WhisperX transcription ---
        # TODO: Replace with actual WhisperX call
        transcript_path = os.path.join(file_folder, 'transcript.txt')
        with open(transcript_path, 'w') as f:
            f.write(f"[Stub transcript for {fname}]")
        log_action('transcription', {'file': fname, 'output': transcript_path})
        # --- Diarization ---
        # TODO: Replace with actual diarization call
        diarization_path = os.path.join(file_folder, 'diarization.json')
        with open(diarization_path, 'w') as f:
            f.write(f"{{'stub': 'diarization for {fname}'}}")
        log_action('diarization', {'file': fname, 'output': diarization_path})
        # --- Spectral Imaging ---
        # TODO: Replace with actual spectral imaging call
        spectrogram_path = os.path.join(file_folder, 'spectrogram.png')
        with open(spectrogram_path, 'wb') as f:
            f.write(b'')  # Placeholder for image
        log_action('spectrogram', {'file': fname, 'output': spectrogram_path})
        # Move to processed
        ensure_dir(PROCESSED_DIR)
        shutil.copy(dest, os.path.join(PROCESSED_DIR, fname))
    except Exception as e:
        log_action('batch_error', {'file': fname, 'error': str(e)})

def run_batch_processor():
    ensure_dir(PROCESSING_DIR)
    ensure_dir(PROCESSED_DIR)
    ensure_dir(CASES_DIR)
    ensure_dir(QUARANTINE_DIR)
    while True:
        files = [f for f in os.listdir(PROCESSING_DIR) if os.path.isfile(os.path.join(PROCESSING_DIR, f)) and os.path.splitext(f)[1].lower() in ALLOWED_EXTENSIONS]
        if len(files) >= BATCH_SIZE:
            batch = files[:BATCH_SIZE]
            log_action('batch_start', {'files': batch})
            for fname in batch:
                process_file(fname)
            log_action('batch_end', {'files': batch})
        else:
            sleep(POLL_INTERVAL)

if __name__ == "__main__":
    run_batch_processor()
