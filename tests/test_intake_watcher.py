import sys
import forensic_engine.meta.meta_tracker as mt

sys.modules["meta.meta_tracker"] = mt  # noqa: E402
from forensic_engine.intake_watcher import IntakeWatcher  # noqa: E402


def test_is_allowed_file():
    watcher = IntakeWatcher()
    assert watcher.is_allowed_file("test.mp3")
    assert not watcher.is_allowed_file("test.txt")
