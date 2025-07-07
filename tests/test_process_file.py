import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from forensic_engine import batch_processor  # noqa: E402
from forensic_engine.meta import meta_tracker  # noqa: E402


def test_process_file(tmp_path, monkeypatch):
    """Process one queued file end-to-end."""
    processing = tmp_path / "processing"
    processed = tmp_path / "processed"
    cases = tmp_path / "cases"
    quarantine = tmp_path / "quarantine"
    for d in (processing, processed, cases, quarantine):
        d.mkdir()
    monkeypatch.setattr(batch_processor, "PROCESSING_DIR", str(processing))
    monkeypatch.setattr(batch_processor, "PROCESSED_DIR", str(processed))
    monkeypatch.setattr(batch_processor, "CASES_DIR", str(cases))
    monkeypatch.setattr(batch_processor, "QUARANTINE_DIR", str(quarantine))
    monkeypatch.setattr(batch_processor, "BATCH_SIZE", 1)
    fname = "case_001_test.wav"
    (processing / fname).write_text("x")
    meta_tracker.META_TRACKER_FILE = str(tmp_path / "log.json")
    batch_processor.process_file(fname)
    file_folder = cases / "case_001" / "audio" / "case_001_test"
    assert (file_folder / "original.wav").exists()
    assert (processed / fname).exists()
