"""
scanner.py
Advanced directory scanning utilities for forensic processing.
"""

import asyncio
import hashlib
import os
from typing import Dict, List, Set

from .meta.meta_tracker import log_action


def collect_file_info(path: str) -> Dict[str, str]:
    """Return metadata and SHA256 hash for a file."""
    info = {
        "path": path,
        "size": os.path.getsize(path),
        "modified": os.path.getmtime(path),
    }
    sha256 = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            sha256.update(chunk)
    info["sha256"] = sha256.hexdigest()
    log_action("file_scanned", {"path": path})
    return info


def scan_directory(root: str, allowed_extensions: Set[str]) -> List[Dict[str, str]]:
    """Recursively scan ``root`` for files with ``allowed_extensions``."""
    results: List[Dict[str, str]] = []
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if os.path.splitext(name)[1].lower() in allowed_extensions:
                full_path = os.path.join(dirpath, name)
                results.append(collect_file_info(full_path))
    return results


async def scan_directory_async(
    root: str, allowed_extensions: Set[str]
) -> List[Dict[str, str]]:
    """Asynchronously scan ``root`` for files with ``allowed_extensions``."""
    tasks = []
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if os.path.splitext(name)[1].lower() in allowed_extensions:
                full_path = os.path.join(dirpath, name)
                tasks.append(asyncio.to_thread(collect_file_info, full_path))
    return await asyncio.gather(*tasks)
