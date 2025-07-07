import os
from forensic_engine.case_builder import sanitize_filename, CaseBuilder


def test_sanitize_filename():
    assert sanitize_filename("bad file#.txt") == "bad_file_.txt"


def test_add_file(tmp_path):
    builder = CaseBuilder(base_dir=str(tmp_path))
    src = tmp_path / "raw data?.wav"
    src.write_text("data")
    dest = builder.add_file(str(src), "case_001", "audio")
    expected = tmp_path / "case_001" / "audio" / "raw_data_.wav"
    assert dest == str(expected)
    assert expected.exists()
