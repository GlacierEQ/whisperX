"""File renamer for standard case naming."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from forensic_engine.utils import validate_case_id


def rename_file(
    path: str,
    case_id: str,
    doc_type: str,
    version: int = 1,
    ref_date: date | None = None,
) -> str:
    """Rename *path* to "{case_id}_{doc_type}_{YYYY-MM-DD}_v{version}{ext}" and return the new path."""
    validate_case_id(case_id)
    ref_date = ref_date or date.today()
# Import os.path for secure path handling
# Import pathlib for Path objects
import os.path
from pathlib import Path

def rename_file(
    path: str,
    case_id: str,
    doc_type: str,
    version: int = 1,
    ref_date: date | None = None,
) -> str:
    """Rename *path* to "{case_id}_{doc_type}_{YYYY-MM-DD}_v{version}{ext}" and return the new path."""
    validate_case_id(case_id)
    ref_date = ref_date or date.today()
    
    # Use os.path.abspath to get the absolute path and prevent path traversal
    abs_path = os.path.abspath(path)
    path_obj = Path(abs_path)
    
    if not path_obj.exists():
        raise FileNotFoundError(path)
    new_name = (
        f"{case_id}_{doc_type}_{ref_date.isoformat()}_v{version}{path_obj.suffix}"
    )
    new_path = path_obj.with_name(new_name)
    if not path_obj.exists():
        raise FileNotFoundError(path)
    new_name = (
        f"{case_id}_{doc_type}_{ref_date.isoformat()}_v{version}{path_obj.suffix}"
    )
    new_path = path_obj.with_name(new_name)
    path_obj.rename(new_path)
    return str(new_path)
