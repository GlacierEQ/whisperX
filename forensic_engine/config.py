"""Central configuration for forensic engine pipeline."""

INTAKE_DIR = "intake"
PROCESSING_DIR = "processing"
PROCESSED_DIR = "processing/processed"
CASES_DIR = "cases"
QUARANTINE_DIR = "quarantine"

BATCH_SIZE = 3
POLL_INTERVAL = 10
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

WHISPER_MODEL = "large-v2"
PYANNOTE_MODEL = "pyannote/speaker-diarization"

ENABLE_SUMMARY = True
ENABLE_LEGAL_SCAN = True
ENABLE_PSYCH_ANALYSIS = True
ENABLE_SOC_ANALYSIS = True
ENABLE_MINDMAP = True
ENABLE_FLOWCHART = True
