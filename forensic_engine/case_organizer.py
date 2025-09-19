"""case_organizer.py
Advanced case organization utilities for sorting and renaming files.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable

from .meta.meta_tracker import log_action


@dataclass
class RenameRule:
    """Rule describing how to rename a file based on metadata."""

    case_id: str
    index: int
    original_path: str

    def new_name(self) -> str:
        """Return the new file name."""
        ext = os.path.splitext(self.original_path)[1]
        return f"{self.case_id}_{self.index:04d}{ext}"


class CaseOrganizer:
    """Orchestrates file sorting and renaming into case folders."""

    def __init__(self, cases_dir: str) -> None:
        self.cases_dir = cases_dir

    def organize(self, files: Iterable[str]) -> None:
        """Sort and rename ``files`` into the case directory tree."""
        counters: dict[str, int] = {}
        for path in files:
            case_id = self._extract_case_id(path)
            if case_id not in counters:
                counters[case_id] = 0
            counters[case_id] += 1
            rule = RenameRule(case_id, counters[case_id], path)
            self._apply_rule(rule)

    def _extract_case_id(self, path: str) -> str:
        """Return case ID derived from ``path`` or use ``unknown_case``."""
        name = os.path.basename(path)
        parts = name.split("_")
        for i, part in enumerate(parts):
            if part == "case" and i + 1 < len(parts):
                next_part = parts[i + 1]
                if next_part.isdigit():
                    return f"case_{next_part}"
            if part.startswith("case"):
                return part
        return "unknown_case"

    def _apply_rule(self, rule: RenameRule) -> None:
        """Move and rename a file using ``rule``."""
        dest_dir = os.path.join(self.cases_dir, rule.case_id, "raw")
        os.makedirs(dest_dir, exist_ok=True)
        new_path = os.path.join(dest_dir, rule.new_name())
        os.replace(rule.original_path, new_path)
        log_action(
            "file_organized",
            {"from": rule.original_path, "to": new_path, "case_id": rule.case_id},
        )
