import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from forensic_engine.utils import ensure_dir, validate_case_id  # noqa: E402


def test_ensure_dir(tmp_path):
    """Create nested directories as needed."""
    target = tmp_path / "a" / "b"
    ensure_dir(target)
    assert target.exists()


def test_validate_case_id_valid():
    """Validate a correct case identifier."""
    validate_case_id("case_001")


def test_validate_case_id_invalid():
    """Reject invalid case identifiers."""
    with pytest.raises(ValueError):
        validate_case_id("bad!id")
