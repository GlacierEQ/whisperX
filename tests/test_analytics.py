import sys
import forensic_engine.config as cfg
import forensic_engine.meta.meta_tracker as mt

sys.modules["config"] = cfg  # noqa: E402
sys.modules["meta.meta_tracker"] = mt  # noqa: E402
from forensic_engine import analytics  # noqa: E402


def test_run_analytics(tmp_path, monkeypatch):
    case_dir = tmp_path / "cases"
    monkeypatch.setattr(analytics, "CASES_DIR", str(case_dir))
    for opt in (
        "ENABLE_SUMMARY",
        "ENABLE_LEGAL_SCAN",
        "ENABLE_PSYCH_ANALYSIS",
        "ENABLE_SOC_ANALYSIS",
        "ENABLE_MINDMAP",
        "ENABLE_FLOWCHART",
    ):
        monkeypatch.setattr(analytics, opt, True)

    logs = []
    monkeypatch.setattr(analytics, "log_action", lambda *a, **k: logs.append((a, k)))

    file_folder = case_dir / "c1" / "audio" / "f1"
    file_folder.mkdir(parents=True)
    analytics.run_analytics("c1", "f1")

    expected_files = [
        "summary.txt",
        "legal_scan.txt",
        "psych_analysis.txt",
        "soc_analysis.txt",
        "mindmap.png",
        "flowchart.png",
    ]
    for fname in expected_files:
        assert (file_folder / fname).exists()
    assert len(logs) >= len(expected_files)
