import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from forensic_engine.case_builder import CaseBuilder, parse_case_id  # noqa: E402


def test_parse_case_id_basic():
    """Extract case identifier from filename."""
    assert parse_case_id("foo_case_1.wav") == "case_1"
    assert parse_case_id("case999_audio.mp3") == "case999"


def test_parse_case_id_invalid():
    """Raise when a case identifier cannot be determined."""
    with pytest.raises(ValueError):
        parse_case_id("randomfile.wav")


def test_ingest_evidence(tmp_path, monkeypatch):
    """Rename and move a file into the organized case structure."""
    builder = CaseBuilder(base_dir=str(tmp_path))
    monkeypatch.setattr(
        "forensic_engine.meta.meta_tracker.META_TRACKER_FILE",
        str(tmp_path / "log.json"),
    )
    monkeypatch.setattr(
        "forensic_engine.case_builder.rename_file",
        lambda p, case_id, doc_type: str(
            Path(p).rename(Path(p).with_name(f"{case_id}_{doc_type}.wav"))
        ),
    )
    src = tmp_path / "case_123_raw.wav"
    src.write_bytes(b"data")
    dest = Path(builder.ingest_evidence(str(src)))
    assert dest.exists()
    assert dest.parent.name == "audio"
    checksum_file = dest.with_suffix(dest.suffix + ".sha256")
    assert checksum_file.exists()
    digest = checksum_file.read_text()
    assert len(digest) == 64
