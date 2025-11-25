import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # noqa: E402
import hashlib  # noqa: E402
import pytest  # noqa: E402
from forensic_engine.scanner import (  # noqa: E402
    collect_file_info,
    scan_directory,
    scan_directory_async,
)


def test_collect_file_info(tmp_path):
    sample = tmp_path / "sample.txt"
    data = b"hello world"
    sample.write_bytes(data)
    info = collect_file_info(str(sample))
    assert info["size"] == len(data)
    assert info["sha256"] == hashlib.sha256(data).hexdigest()


def test_scan_directory(tmp_path):
    allowed = {".txt"}
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b.bin").write_text("b")
    results = scan_directory(str(tmp_path), allowed)
    paths = {r["path"] for r in results}
    assert str(tmp_path / "a.txt") in paths
    assert str(tmp_path / "b.bin") not in paths


@pytest.mark.asyncio
async def test_scan_directory_async(tmp_path):
    allowed = {".txt"}
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b.bin").write_text("b")
    results = await scan_directory_async(str(tmp_path), allowed)
    paths = {r["path"] for r in results}
    assert str(tmp_path / "a.txt") in paths
    assert str(tmp_path / "b.bin") not in paths
