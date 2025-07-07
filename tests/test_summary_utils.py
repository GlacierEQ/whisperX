import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))


def test_summarize_basic():
    """Summarize multiple sentences down to two."""
    from forensic_engine.summary_utils import summarize  # noqa: E402

    text = (
        "Alpha bravo charlie. Delta echo foxtrot. "
        "Golf hotel india. Juliet kilo lima."
    )
    result = summarize(text, max_sentences=2)
    assert result == "Alpha bravo charlie. Delta echo foxtrot."


def test_summarize_short():
    """Return the original when input has fewer sentences than limit."""
    from forensic_engine.summary_utils import summarize  # noqa: E402

    text = "Alpha bravo."
    assert summarize(text, max_sentences=3) == "Alpha bravo."


def test_summarize_empty():
    """Return empty string when input is blank."""
    from forensic_engine.summary_utils import summarize  # noqa: E402

    assert summarize("", max_sentences=2) == ""
