"""Forensic Transcriber

A toolkit for processing, transcribing, and analyzing audio or video with
forensic integrity. Features include speaker diarization, person identification
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
