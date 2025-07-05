#!/usr/bin/env python3
"""Modular repository maintenance script."""
from __future__ import annotations

import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Iterable, List

LOGFILE = Path("setup_script.log")
OUTDATED_LOG = Path("outdated_deps.json")
CONFIG_FILE = Path("maintenance_config.json")


def log(message: str) -> None:
    """Append a timestamped message to the log file."""
    with LOGFILE.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.utcnow().isoformat()} - {message}\n")


def run(command: str) -> subprocess.CompletedProcess:
    """Run a shell command and log its output."""
    log(f"Running: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
        )
        log(result.stdout)
    except subprocess.CalledProcessError as e:
        log(f"Command failed with return code {e.returncode}")
        log(e.output)
        raise
    return result
    """Run a shell command and log its output."""
    log(f"Running: {command}")
    result = subprocess.run(
        command,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    log(result.stdout)
    return result


def check_outdated() -> None:
    """Check for outdated pip packages and log to JSON file."""
    result = run("pip list --outdated --format=json")
    data = json.loads(result.stdout) if result.returncode == 0 else []
    OUTDATED_LOG.write_text(json.dumps(data, indent=2), encoding="utf-8")
    log(f"Outdated dependencies written to {OUTDATED_LOG}")


@dataclass
class Task:
    name: str
    action: Callable[[], None]
    continue_on_fail: bool = True

    def run(self) -> None:
        log(f"Starting {self.name}")
        try:
            self.action()
        except Exception as exc:  # noqa: BLE001
            log(f"Task {self.name} failed: {exc}")
            if not self.continue_on_fail:
                raise
        finally:
            log(f"Finished {self.name}")


def default_tasks() -> List[Task]:
    return [
        Task("check_outdated", check_outdated),
        Task("black", lambda: run("black .")),
        Task("flake8", lambda: run("flake8")),
        Task("tests", lambda: run("pytest tests/"), continue_on_fail=False),
    ]


def load_tasks() -> tuple[List[Task], bool]:
    if not CONFIG_FILE.exists():
        return default_tasks(), True
    try:
        config = json.loads(CONFIG_FILE.read_text())
    except json.JSONDecodeError:
        log("Invalid config; using defaults")
        return default_tasks(), True
    tasks: List[Task] = []
    concurrent = config.get("concurrent", True)
    for entry in config.get("tasks", []):
        cmd = entry.get("command")
        if not cmd:
            continue
        name = entry.get("name", cmd)
        cont = entry.get("continue_on_fail", True)
        tasks.append(Task(name, lambda c=cmd: run(c), continue_on_fail=cont))
    return (tasks or default_tasks(), concurrent)


def run_tasks(tasks: Iterable[Task], concurrent: bool = True) -> None:
    if concurrent:
        with ThreadPoolExecutor() as exc:
            list(exc.map(lambda t: t.run(), tasks))
    else:
        for task in tasks:
            task.run()


def main() -> None:
    tasks, concurrent = load_tasks()
    run_tasks(tasks, concurrent)
    log("Maintenance tasks complete")


if __name__ == "__main__":
    main()
