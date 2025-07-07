"""
meta_tracker.py
Meta-tracking logic for logging actions, errors, and generating reports.
"""

import json
import os
from datetime import datetime, timezone

META_TRACKER_FILE = os.path.join(os.path.dirname(__file__), "meta-tracker.json")


def log_action(action, details=None):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "details": details or {},
    }
    if os.path.exists(META_TRACKER_FILE):
        with open(META_TRACKER_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(META_TRACKER_FILE, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    log_action("scaffold_created", {"status": "success"})
