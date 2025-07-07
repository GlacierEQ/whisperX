"""Utility functions for text summarization."""

from __future__ import annotations

import re
from collections import Counter

__all__ = ["split_sentences", "summarize"]


def split_sentences(text: str) -> list[str]:
    """Split *text* into sentences using punctuation."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s for s in sentences if s]


def summarize(text: str, max_sentences: int = 3) -> str:
    """Return a simple summary of *text* using sentence scoring."""
    text = text.strip()
    if not text:
        return ""
    sentences = split_sentences(text)
    if len(sentences) <= max_sentences:
        return text
    words = re.findall(r"\w+", text.lower())
    freq = Counter(words)
    scored = []
    for idx, sentence in enumerate(sentences):
        tokens = re.findall(r"\w+", sentence.lower())
        score = sum(freq[t] for t in tokens)
        scored.append((score, idx, sentence))
    top = sorted(scored, key=lambda x: (-x[0], x[1]))[:max_sentences]
    ordered = [s for _, _, s in sorted(top, key=lambda x: x[1])]
    return " ".join(ordered)
