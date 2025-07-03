"""
analytics.py
Run mind mapping and summary generation on finalized transcripts.
Outputs are stored under ``cases/{case_id}/audio/{file_id}/``.
"""

import os
from forensic_engine.config import (
    CASES_DIR,
    ENABLE_SUMMARY,
    ENABLE_LEGAL_SCAN,
    ENABLE_PSYCH_ANALYSIS,
    ENABLE_SOC_ANALYSIS,
    ENABLE_MINDMAP,
    ENABLE_FLOWCHART,
)
from forensic_engine.meta.meta_tracker import log_action


def run_analytics(case_id: str, file_id: str) -> None:
    """Run analytics modules for a processed file."""
    file_folder = os.path.join(CASES_DIR, case_id, "audio", file_id)
    if not os.path.exists(file_folder):
        log_action(
            "analytics_error",
            {"case_id": case_id, "file_id": file_id, "error": "file_folder_missing"},
        )
        return
    if ENABLE_SUMMARY:
        summary_path = os.path.join(file_folder, "summary.txt")
        with open(summary_path, "w") as f:
            f.write(f"[Stub summary for {file_id}]")
        log_action(
            "summary", {"case_id": case_id, "file_id": file_id, "output": summary_path}
        )
    if ENABLE_LEGAL_SCAN:
        legal_path = os.path.join(file_folder, "legal_scan.txt")
        with open(legal_path, "w") as f:
            f.write(f"[Stub legal scan for {file_id}]")
        log_action(
            "legal_scan", {"case_id": case_id, "file_id": file_id, "output": legal_path}
        )
    if ENABLE_PSYCH_ANALYSIS:
        psych_path = os.path.join(file_folder, "psych_analysis.txt")
        with open(psych_path, "w") as f:
            f.write(f"[Stub psych analysis for {file_id}]")
        log_action(
            "psych_analysis",
            {"case_id": case_id, "file_id": file_id, "output": psych_path},
        )
    if ENABLE_SOC_ANALYSIS:
        soc_path = os.path.join(file_folder, "soc_analysis.txt")
        with open(soc_path, "w") as f:
            f.write(f"[Stub soc analysis for {file_id}]")
        log_action(
            "soc_analysis", {"case_id": case_id, "file_id": file_id, "output": soc_path}
        )
    if ENABLE_MINDMAP:
        mindmap_path = os.path.join(file_folder, "mindmap.png")
        with open(mindmap_path, "wb") as f:
            f.write(b"")
        log_action(
            "mindmap", {"case_id": case_id, "file_id": file_id, "output": mindmap_path}
        )
    if ENABLE_FLOWCHART:
        flowchart_path = os.path.join(file_folder, "flowchart.png")
        with open(flowchart_path, "wb") as f:
            f.write(b"")
        log_action(
            "flowchart",
            {"case_id": case_id, "file_id": file_id, "output": flowchart_path},
        )


if __name__ == "__main__":
    pass
