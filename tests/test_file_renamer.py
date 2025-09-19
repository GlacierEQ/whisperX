import os
import sys
from pathlib import Path
from datetime import date
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from forensic_engine.file_renamer import rename_file  # noqa: E402


def test_rename_file(tmp_path):
    src = tmp_path / "source.txt"
    src.write_text("data")
    new_path = rename_file(
        str(src), "CASE1", "Doc", version=2, ref_date=date(2023, 1, 1)
    )
    assert os.path.basename(new_path) == "CASE1_Doc_2023-01-01_v2.txt"
    assert os.path.exists(new_path)


def test_rename_invalid_case(tmp_path):
    src = tmp_path / "a.txt"
    src.write_text("x")
    with pytest.raises(ValueError):
        rename_file(str(src), "bad?", "Doc")
