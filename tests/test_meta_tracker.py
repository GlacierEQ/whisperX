import json
from forensic_engine.meta import meta_tracker


def test_log_action_creates_file(tmp_path, monkeypatch):
    log_file = tmp_path / "meta.json"
    monkeypatch.setattr(meta_tracker, "META_TRACKER_FILE", str(log_file))
    meta_tracker.log_action("test", {"a": 1})
    assert log_file.exists()
    data = json.loads(log_file.read_text())
    assert data[0]["action"] == "test"
    assert data[0]["details"]["a"] == 1
