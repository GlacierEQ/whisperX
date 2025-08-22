# WhisperX Forensic Pipeline

This repository contains a modular forensic processing pipeline built around WhisperX transcription. It provides tooling for collecting audio and video evidence, running batch processing, and organizing results under case directories.

## Features

- Automated intake watching and batch processing
- Case routing with per-file folders
- Basic analytics stubs (summary, legal scan, psychological and sociological analysis)
- Meta tracking for actions and errors
- Input validation for case identifiers

## Usage

1. Place files in the `intake/` directory.
2. Run `python forensic_engine/intake_watcher.py` to monitor incoming files.
3. Run `python forensic_engine/batch_processor.py` to process queued files.

All output is organized under `cases/{case_id}/` with subfolders for audio, transcripts, and analysis outputs.

## Development

Lint and format the code with **Black** and **Flake8**. Run tests with **pytest** from the repository root:

```bash
black .
flake8
pytest tests/
```
