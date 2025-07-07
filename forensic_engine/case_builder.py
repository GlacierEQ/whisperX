"""Case organization utilities for the forensic engine."""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path

from forensic_engine.file_renamer import rename_file
from forensic_engine.meta.meta_tracker import log_action
from forensic_engine.utils import ensure_dir, validate_case_id

DOC_TYPE_MAP = {
    ".txt": "transcript",
    ".wav": "audio",
    ".mp3": "audio",
    ".m4a": "audio",
    ".mp4": "video",
    ".mov": "video",
    ".pdf": "document",
}


def parse_case_id(filename: str) -> str:
    """Return the case identifier parsed from *filename*."""
    parts = Path(filename).stem.split("_")
    for idx, part in enumerate(parts):
        if part == "case" and idx + 1 < len(parts):
            return f"case_{parts[idx + 1]}"
        if part.startswith("case") and part[4:].isdigit():
            return part
    raise ValueError(f"cannot determine case id from {filename}")


@dataclass
class CaseBuilder:
    """Build and organize evidence case folders."""

    base_dir: str = "cases"

    def ingest_evidence(self, path: str) -> str:
        """Rename *path* and move it into the case folder."""
        case_id = parse_case_id(os.path.basename(path))
        validate_case_id(case_id)
        ensure_dir(self.base_dir)
        ext = Path(path).suffix.lower()
        doc_type = DOC_TYPE_MAP.get(ext, "misc")
        case_folder = Path(self.base_dir) / case_id / doc_type
        ensure_dir(case_folder)
        renamed = rename_file(path, case_id, doc_type)
        dest = case_folder / Path(renamed).name
        Path(renamed).replace(dest)
        checksum = self._write_checksum(dest)
        log_action(
            "case_ingest", {"case_id": case_id, "file": str(dest), "checksum": checksum}
        )
        return str(dest)

    def _write_checksum(self, path: Path) -> str:
        """Write a SHA256 checksum file for *path* and return the digest."""
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        checksum_file = path.with_suffix(path.suffix + ".sha256")
        checksum_file.write_text(digest)
        return digest
