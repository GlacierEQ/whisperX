from forensic_engine import case_router


def test_route_file(tmp_path, monkeypatch):
    case_dir = tmp_path / "cases"
    monkeypatch.setattr(case_router, "CASES_DIR", str(case_dir))
    router = case_router.CaseRouter()
    src = tmp_path / "src.txt"
    src.write_text("data")
    router.route_file(str(src), "case1", "audio")
    dest = case_dir / "case1" / "audio" / "src.txt"
    assert dest.exists()
    assert not src.exists()


def test_route_file_sanitizes(tmp_path, monkeypatch):
    case_dir = tmp_path / "cases"
    monkeypatch.setattr(case_router, "CASES_DIR", str(case_dir))
    router = case_router.CaseRouter()
    src = tmp_path / "bad name#.txt"
    src.write_text("data")
    router.route_file(str(src), "case1", "audio")
    dest = case_dir / "case1" / "audio" / "bad_name_.txt"
    assert dest.exists()


def test_route_batch(tmp_path, monkeypatch):
    case_dir = tmp_path / "cases"
    monkeypatch.setattr(case_router, "CASES_DIR", str(case_dir))
    router = case_router.CaseRouter()
    f1 = tmp_path / "a.txt"
    f2 = tmp_path / "b.txt"
    f1.write_text("a")
    f2.write_text("b")
    mapping = {str(f1): ("c1", "audio"), str(f2): ("c2", "transcripts")}
    router.route_batch([str(f1), str(f2)], mapping)
    assert (case_dir / "c1" / "audio" / "a.txt").exists()
    assert (case_dir / "c2" / "transcripts" / "b.txt").exists()
