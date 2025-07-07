import json
import sys
from pathlib import Path
from importlib import reload

sys.path.append(str(Path(__file__).resolve().parents[1]))

import forensic_engine.meta.meta_tracker as mt  # noqa: E402


def test_log_action(tmp_path):
    """Write an action entry to the tracker log."""
    mt.META_TRACKER_FILE = str(tmp_path / "log.json")
    reload(mt)
    mt.log_action("test", {"a": 1})
    data = json.loads(Path(mt.META_TRACKER_FILE).read_text())
    assert data[0]["action"] == "test"
