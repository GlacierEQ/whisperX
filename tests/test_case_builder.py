import sys
import pathlib
import os

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # noqa: E402
from forensic_engine.case_builder import CaseOrganizer  # noqa: E402


def test_case_organizer(tmp_path):
    files = []
    for idx in range(3):
        fname = tmp_path / f"case_001_audio_{idx}.wav"
        fname.write_text("x")
        files.append(str(fname))
    org = CaseOrganizer(str(tmp_path / "cases"))
    org.organize(files)
    dest = tmp_path / "cases" / "case_001" / "raw" / "case_001_0003.wav"
    assert dest.exists()

    assert not any(os.path.exists(p) for p in files)
