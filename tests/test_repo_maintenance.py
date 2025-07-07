import json
import sys
from pathlib import Path
import importlib.util
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "repo_maintenance", ROOT / "repo_maintenance.py"
)
rm = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = rm
spec.loader.exec_module(rm)


def test_run_tasks_sequential(tmp_path):
    log_file = tmp_path / "log.txt"
    rm.LOGFILE = log_file
    called = []

    def task1():
        called.append("task1")

    def task2():
        called.append("task2")

    tasks = [rm.Task("t1", task1), rm.Task("t2", task2)]
    rm.run_tasks(tasks, concurrent=False)

    assert called == ["task1", "task2"]
    assert log_file.read_text().count("Starting") == 2


def test_load_tasks_defaults(tmp_path):
    cfg = tmp_path / "config.json"
    with patch.object(rm, "CONFIG_FILE", cfg):
        tasks, concurrent = rm.load_tasks()
    assert concurrent is True
    assert any(t.name == "black" for t in tasks)


def test_check_outdated_writes_json(tmp_path, monkeypatch):
    rm.OUTDATED_LOG = tmp_path / "outdated.json"

    def fake_run(cmd):
        return rm.subprocess.CompletedProcess(cmd, 0, "[]")

    monkeypatch.setattr(rm, "run", fake_run)
    rm.check_outdated()
    assert rm.OUTDATED_LOG.exists()
    text = rm.OUTDATED_LOG.read_text()
    assert text in {"[]", "[]\n"}


def test_run_logs_output(monkeypatch, tmp_path):
    rm.LOGFILE = tmp_path / "log.txt"

    class FakeCompleted:
        def __init__(self):
            self.returncode = 0
            self.stdout = "hi"

    def fake_subprocess(*args, **kwargs):
        return FakeCompleted()

    monkeypatch.setattr(rm.subprocess, "run", fake_subprocess)
    result = rm.run("echo hi")
    assert result.stdout == "hi"
    assert "Running: echo hi" in rm.LOGFILE.read_text()


def test_run_tasks_stop_on_fail(monkeypatch, tmp_path):
    rm.LOGFILE = tmp_path / "log.txt"

    def bad():
        raise RuntimeError("fail")

    t1 = rm.Task("good", lambda: None)
    t2 = rm.Task("bad", bad, continue_on_fail=False)
    with pytest.raises(RuntimeError):
        rm.run_tasks([t1, t2], concurrent=False)
    log = rm.LOGFILE.read_text()
    assert "Starting bad" in log


def test_load_tasks_from_config(tmp_path):
    config = {
        "concurrent": False,
        "tasks": [
            {"name": "a", "command": "echo a"},
            {"command": "echo b", "continue_on_fail": False},
        ],
    }
    cfg = tmp_path / "cfg.json"
    cfg.write_text(json.dumps(config))
    with patch.object(rm, "CONFIG_FILE", cfg):
        tasks, concurrent = rm.load_tasks()
    assert concurrent is False
    assert len(tasks) == 2
    assert tasks[1].continue_on_fail is False


def test_run_tasks_concurrent(tmp_path):
    rm.LOGFILE = tmp_path / "log.txt"
    called = set()

    def task_a():
        called.add("a")

    def task_b():
        called.add("b")

    rm.run_tasks([rm.Task("a", task_a), rm.Task("b", task_b)], concurrent=True)
    assert called == {"a", "b"}


def test_main(monkeypatch, tmp_path):
    executed = []

    def fake_load():
        return ([rm.Task("a", lambda: executed.append("a"))], False)

    monkeypatch.setattr(rm, "load_tasks", fake_load)
    rm.LOGFILE = tmp_path / "log.txt"
    rm.main()
    assert executed == ["a"]
