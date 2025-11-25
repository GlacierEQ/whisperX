# Forensic Engine Scaffold

This project is a modular, extensible forensic processing pipeline for WhisperX transcription and advanced analytics.

## Directory Structure

- `intake/` — Watched for new audio/video files.
- `processing/` — Staging area for batch processing.
- `cases/` — Hierarchical case file storage.
- `meta/` — Meta-tracking and logs.
- `intake_watcher.py` — Monitors intake, moves files to processing.
- `batch_processor.py` — Processes files in batches (transcription, diarization, spectral, renaming).
- `case_router.py` — Routes processed files to correct case folders.
- `analytics.py` — Runs mind mapping, summaries, legal/psych/soc analysis.
- `utils.py` — Shared utilities.
- `scanner.py` — High powered directory scanning utilities.
- `meta/meta_tracker.py` — Meta-tracking logic.
- `meta/meta-tracker.json` — Meta-tracker log file.

## Next Steps
- Implement each module in order of pipeline flow.
- Integrate WhisperX and analytics tools.
- Expand meta-tracking and reporting.
- Develop unit tests for scanner utilities.
