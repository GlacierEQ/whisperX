import os
import sys
import forensic_engine.config as cfg
import forensic_engine.meta.meta_tracker as mt

sys.modules["config"] = cfg  # noqa: E402
sys.modules["meta.meta_tracker"] = mt  # noqa: E402
from forensic_engine import batch_processor  # noqa: E402


def test_get_case_id():
    assert batch_processor.get_case_id("case_001_audio_1234.wav") == "case_001"
    assert batch_processor.get_case_id("no_case.wav") is None


def test_process_file(tmp_path, monkeypatch):
    processing = tmp_path / "processing"
    processed = tmp_path / "processed"
    cases = tmp_path / "cases"
    quarantine = tmp_path / "quarantine"
    for p in (processing, processed, cases, quarantine):
        p.mkdir()

    fname = "case_001_test.wav"
    (processing / fname).write_text("data")

    monkeypatch.setattr(batch_processor, "PROCESSING_DIR", str(processing))
    monkeypatch.setattr(batch_processor, "PROCESSED_DIR", str(processed))
    monkeypatch.setattr(batch_processor, "CASES_DIR", str(cases))
    monkeypatch.setattr(batch_processor, "QUARANTINE_DIR", str(quarantine))
    monkeypatch.setattr(batch_processor, "ALLOWED_EXTENSIONS", {".wav"})

    actions = []
    monkeypatch.setattr(
        batch_processor, "log_action", lambda *a, **k: actions.append((a, k))
    )

    batch_processor.process_file(fname)

    file_id = os.path.splitext(fname)[0]
    folder = cases / "case_001" / "audio" / file_id
    assert (folder / "transcript.txt").exists()
    assert (processed / fname).exists()
    assert any(a[0][0] == "file_routed" for a in actions)


def test_process_batch(monkeypatch):
    calls = []
    monkeypatch.setattr(batch_processor, "process_file", lambda f: calls.append(f))
    batch_processor.process_batch(["a", "b", "c"])
    assert calls == ["a", "b", "c"]
