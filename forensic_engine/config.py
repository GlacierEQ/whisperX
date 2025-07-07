"""Central configuration for the forensic engine pipeline."""

import os

# Directories
INTAKE_DIR = "intake"
PROCESSING_DIR = "processing"
PROCESSED_DIR = "processing/processed"
CASES_DIR = "cases"
QUARANTINE_DIR = "quarantine"

# Batch processing
BATCH_SIZE = 3
# Number of parallel workers for batch processing
NUM_WORKERS = int(os.getenv("NUM_WORKERS", "4"))
POLL_INTERVAL = 10  # seconds
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

# WhisperX/pyannote/analytics model paths (set as needed)
WHISPER_MODEL = "large-v2"
PYANNOTE_MODEL = "pyannote/speaker-diarization"

# Analytics modules (enable/disable)
ENABLE_SUMMARY = True
ENABLE_LEGAL_SCAN = True
ENABLE_PSYCH_ANALYSIS = True
ENABLE_SOC_ANALYSIS = True
ENABLE_MINDMAP = True
ENABLE_FLOWCHART = True
