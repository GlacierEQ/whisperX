import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from forensic_engine import intake_watcher as iw  # noqa: E402
from forensic_engine.intake_watcher import IntakeWatcher  # noqa: E402


def test_is_allowed_file():
    """Determine whether a filename passes the extension filter."""
    watcher = IntakeWatcher()
    assert watcher.is_allowed_file("test.mp3")
    assert not watcher.is_allowed_file("test.txt")


def test_watch_moves_file(tmp_path, monkeypatch):
    """Move allowed files from intake to processing."""
    intake = tmp_path / "intake"
    processing = tmp_path / "processing"
    intake.mkdir()
    processing.mkdir()
    monkeypatch.setattr(iw, "INTAKE_DIR", str(intake))
    monkeypatch.setattr(iw, "PROCESSING_DIR", str(processing))
    (intake / "sample.mp3").write_text("x")
    watcher = iw.IntakeWatcher(poll_interval=0)

    def fake_sleep(_):
        raise RuntimeError

    monkeypatch.setattr(iw, "sleep", fake_sleep)
    with pytest.raises(RuntimeError):
        watcher.watch()
    assert not (intake / "sample.mp3").exists()
    assert (processing / "sample.mp3").exists()
