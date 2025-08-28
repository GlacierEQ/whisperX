"""summary_utils.py
Utilities for text summarization.
"""

import re
from collections import Counter


def split_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    return re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)


def summarize(text: str, num_sentences: int = 3) -> str:
    """Generate a summary of the text using a frequency-based approach."""
    if not text:
        return ""

    sentences = split_sentences(text)
    if len(sentences) <= num_sentences:
        return text

    # Simple word frequency counter (ignoring case and punctuation)
    words = re.findall(r"\w+", text.lower())
    word_freq = Counter(words)

    # Score sentences based on word frequency
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        sentence_words = re.findall(r"\w+", sentence.lower())
        score = sum(word_freq[word] for word in sentence_words)
        sentence_scores[i] = score

    # Get the top N sentences
    top_sentence_indices = sorted(
        sentence_scores, key=sentence_scores.get, reverse=True
    )[:num_sentences]
    top_sentence_indices.sort()  # Keep original order

    summary = " ".join(sentences[i] for i in top_sentence_indices)
    return summary
