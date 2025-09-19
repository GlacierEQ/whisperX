import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from forensic_engine.case_router import CaseRouter  # noqa: E402


def test_route_file(tmp_path, monkeypatch):
    monkeypatch.setattr("forensic_engine.case_router.CASES_DIR", str(tmp_path))
    src = tmp_path / "f.txt"
    src.write_text("d")
    router = CaseRouter()
    router.route_file(str(src), "case_a", "audio")
    dest = tmp_path / "case_a" / "audio" / "f.txt"
    assert dest.exists()


def test_route_batch(tmp_path, monkeypatch):
    monkeypatch.setattr("forensic_engine.case_router.CASES_DIR", str(tmp_path))
    src1 = tmp_path / "a.txt"
    src2 = tmp_path / "b.txt"
    src1.write_text("x")
    src2.write_text("y")
    mapping = {str(src1): ("case1", "docs"), str(src2): ("case2", "audio")}
    router = CaseRouter()
    router.route_batch([str(src1), str(src2)], mapping)
    assert (tmp_path / "case1" / "docs" / "a.txt").exists()
    assert (tmp_path / "case2" / "audio" / "b.txt").exists()
