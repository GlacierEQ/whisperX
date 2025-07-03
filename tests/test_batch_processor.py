import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from forensic_engine.batch_processor import get_case_id, ensure_dir  # noqa: E402


def test_get_case_id():
    assert get_case_id("case_001_audio.wav") == "case_001"
    assert get_case_id("no_case.wav") is None


def test_ensure_dir(tmp_path):
    target = tmp_path / "subdir"
    ensure_dir(target)
    assert target.exists()


def test_get_case_id_variants():
    assert get_case_id("foo_case_123.wav") == "case_123"
    assert get_case_id("case999_video.mp4") == "case999"
