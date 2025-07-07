import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from forensic_engine.file_renamer import rename_file  # noqa: E402


def test_rename_missing(tmp_path):
    """Fail when the target file does not exist."""
    missing = tmp_path / "nope.txt"
    with pytest.raises(FileNotFoundError):
        rename_file(str(missing), "CASE", "Doc")
