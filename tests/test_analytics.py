import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import forensic_engine.analytics as analytics  # noqa: E402
from forensic_engine.meta import meta_tracker  # noqa: E402


def test_run_analytics(tmp_path, monkeypatch):
    base = tmp_path / "cases"
    file_folder = base / "case_001" / "audio" / "file_1"
    file_folder.mkdir(parents=True)
    monkeypatch.setattr(analytics, "CASES_DIR", str(base))
    monkeypatch.setattr(analytics, "ENABLE_SUMMARY", True)
    monkeypatch.setattr(analytics, "ENABLE_LEGAL_SCAN", True)
    monkeypatch.setattr(analytics, "ENABLE_PSYCH_ANALYSIS", True)
    monkeypatch.setattr(analytics, "ENABLE_SOC_ANALYSIS", True)
    monkeypatch.setattr(analytics, "ENABLE_MINDMAP", True)
    monkeypatch.setattr(analytics, "ENABLE_FLOWCHART", True)
    meta_tracker.META_TRACKER_FILE = str(tmp_path / "log.json")
    analytics.run_analytics("case_001", "file_1")
    outputs = [
        "summary.txt",
        "legal_scan.txt",
        "psych_analysis.txt",
        "soc_analysis.txt",
        "mindmap.png",
        "flowchart.png",
    ]
    for name in outputs:
        assert (file_folder / name).exists()
    data = json.loads(Path(meta_tracker.META_TRACKER_FILE).read_text())
    assert any(e["action"] == "summary" for e in data)
