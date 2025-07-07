import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from forensic_engine import batch_processor  # noqa: E402
from forensic_engine.meta import meta_tracker  # noqa: E402


def test_run_batch_processor(tmp_path, monkeypatch):
    """Run the batch processor loop once and move files."""
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
    monkeypatch.setattr(batch_processor, "POLL_INTERVAL", 0)
    (processing / "case_001_audio.wav").write_text("x")
    meta_tracker.META_TRACKER_FILE = str(tmp_path / "log.json")

    def fake_sleep(_):
        raise RuntimeError

    monkeypatch.setattr(batch_processor, "sleep", fake_sleep)
    with pytest.raises(RuntimeError):
        batch_processor.run_batch_processor()
    assert (processed / "case_001_audio.wav").exists()
