from forensic_engine import utils


def test_ensure_dir(tmp_path):
    target = tmp_path / "newdir"
    utils.ensure_dir(target)
    assert target.is_dir()
