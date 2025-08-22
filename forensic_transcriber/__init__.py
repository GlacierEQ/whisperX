"""
Forensic Transcriber - A comprehensive forensic audio/video transcription and analysis system.

This module provides tools for processing, transcribing, and analyzing audio/video files
with forensic integrity, including features like speaker diarization, person identification,
and comprehensive metadata logging.
"""

__version__ = "0.1.0"
__author__ = "Casey C. (GlacierEQ)"
__license__ = "MIT"

# Import core functionality
from .core.processor import process_media  # noqa: F401
from .core.scanner import scan_directory  # noqa: F401
from .models.case import Case  # noqa: F401

# Set up logging
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
