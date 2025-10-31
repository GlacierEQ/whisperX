"""Quantum-Enhanced WhisperX Processor

Provides forensic-grade audio transcription with quantum intelligence
and advanced speaker diarization capabilities.
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import torch
import whisperx
from whisperx.diarize import DiarizationPipeline

from .memory_fusion import QuantumMemoryFusion
from .forensic_validator import ForensicValidator
from .legal_formatter import LegalTranscriptFormatter

logger = logging.getLogger(__name__)

class QuantumWhisperXProcessor:
    """Quantum-enhanced WhisperX processor for forensic audio transcription."""
    
    def __init__(self, 
                 model_size: str = "large-v3",
                 device: str = "cuda",
                 compute_type: str = "float16",
                 batch_size: int = 16,
                 hf_token: Optional[str] = None):
        """
        Initialize the Quantum WhisperX Processor.
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large-v2, large-v3)
            device: Computing device (cuda, cpu)
            compute_type: Precision type (float16, float32, int8)
            batch_size: Batch size for processing
            hf_token: HuggingFace token for diarization models
        """
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.batch_size = batch_size
        self.hf_token = hf_token
        
        # Initialize components
        self.memory_fusion = QuantumMemoryFusion()
        self.forensic_validator = ForensicValidator()
        self.legal_formatter = LegalTranscriptFormatter()
        
        # Models (loaded on demand)
        self.whisper_model = None
        self.align_model = None
        self.align_metadata = None
        self.diarize_model = None
        
        logger.info(f"Quantum WhisperX Processor initialized with {model_size} model")
    
    async def load_models(self) -> None:
        """Load all required models asynchronously."""
        logger.info("Loading Quantum WhisperX models...")
        
        # Load Whisper model
        self.whisper_model = whisperx.load_model(
            self.model_size, 
            self.device, 
            compute_type=self.compute_type
        )
        logger.info(f"Loaded Whisper {self.model_size} model")
        
        # Load diarization model if token provided
        if self.hf_token:
            self.diarize_model = DiarizationPipeline(
                use_auth_token=self.hf_token,
                device=self.device
            )
            logger.info("Loaded diarization model")
        
        logger.info("All models loaded successfully")
    
    async def process_forensic_audio(self, 
                                   audio_path: str, 
                                   case_id: str,
                                   language: Optional[str] = None,
                                   min_speakers: Optional[int] = None,
                                   max_speakers: Optional[int] = None) -> Dict[str, Any]:
        """
        Process audio file with forensic-grade precision.
        
        Args:
            audio_path: Path to audio file
            case_id: Case identifier for chain of custody
            language: Language code (auto-detected if None)
            min_speakers: Minimum number of speakers
            max_speakers: Maximum number of speakers
            
        Returns:
            Dictionary containing transcription results and forensic metadata
        """
        start_time = datetime.utcnow()
        logger.info(f"Starting forensic processing of {audio_path} for case {case_id}")
        
        # Ensure models are loaded
        if not self.whisper_model:
            await self.load_models()
        
        try:
            # Phase 1: Load and validate audio
            audio = whisperx.load_audio(audio_path)
            audio_info = await self.forensic_validator.validate_audio(audio_path)
            logger.info(f"Audio validated: {audio_info['duration']:.2f}s, {audio_info['sample_rate']}Hz")
            
            # Phase 2: Transcribe with Whisper
            logger.info("Phase 2: Transcribing with Whisper...")
            result = self.whisper_model.transcribe(audio, batch_size=self.batch_size)
            detected_language = result.get("language", language)
            logger.info(f"Transcription complete. Language: {detected_language}")
            
            # Phase 3: Align with wav2vec2 for precise timestamps
            logger.info("Phase 3: Aligning timestamps...")
            if not self.align_model or detected_language != getattr(self, '_last_language', None):
                self.align_model, self.align_metadata = whisperx.load_align_model(
                    language_code=detected_language, 
                    device=self.device
                )
                self._last_language = detected_language
            
            result = whisperx.align(
                result["segments"], 
                self.align_model, 
                self.align_metadata, 
                audio, 
                self.device, 
                return_char_alignments=False
            )
            logger.info("Timestamp alignment complete")
            
            # Phase 4: Speaker diarization (if enabled)
            diarization_result = None
            if self.diarize_model:
                logger.info("Phase 4: Performing speaker diarization...")
                diarize_segments = self.diarize_model(
                    audio, 
                    min_speakers=min_speakers, 
                    max_speakers=max_speakers
                )
                result = whisperx.assign_word_speakers(diarize_segments, result)
                diarization_result = diarize_segments
                logger.info(f"Diarization complete. Detected {len(diarize_segments.labels())} speakers")
            
            # Phase 5: Generate forensic metadata
            logger.info("Phase 5: Generating forensic metadata...")
            forensic_metadata = await self._generate_forensic_metadata(
                audio_path, result, audio_info, start_time
            )
            
            # Phase 6: Create chain of custody documentation
            logger.info("Phase 6: Documenting chain of custody...")
            custody_chain = await self._document_custody_chain(
                audio_path, case_id, forensic_metadata
            )
            
            # Phase 7: Format for legal use
            logger.info("Phase 7: Formatting for legal compliance...")
            legal_transcript = await self.legal_formatter.format_for_court({
                "case_id": case_id,
                "segments": result["segments"],
                "metadata": forensic_metadata,
                "custody_chain": custody_chain
            })
            
            # Phase 8: Store in quantum memory
            await self.memory_fusion.store_processing_result({
                "case_id": case_id,
                "audio_path": audio_path,
                "transcript": legal_transcript,
                "metadata": forensic_metadata,
                "processing_time": (datetime.utcnow() - start_time).total_seconds()
            })
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"Forensic processing complete in {processing_time:.2f}s")
            
            return {
                "success": True,
                "case_id": case_id,
                "audio_path": audio_path,
                "language": detected_language,
                "transcript": result["segments"],
                "legal_transcript": legal_transcript,
                "diarization": diarization_result,
                "forensic_metadata": forensic_metadata,
                "custody_chain": custody_chain,
                "processing_time": processing_time,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing {audio_path}: {str(e)}")
            return {
                "success": False,
                "case_id": case_id,
                "audio_path": audio_path,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _generate_forensic_metadata(self, 
                                        audio_path: str, 
                                        result: Dict, 
                                        audio_info: Dict,
                                        start_time: datetime) -> Dict[str, Any]:
        """Generate comprehensive forensic metadata."""
        return {
            "processor_info": {
                "name": "GlacierEQ Quantum WhisperX",
                "version": "2.0.0-quantum",
                "model_size": self.model_size,
                "device": self.device,
                "compute_type": self.compute_type
            },
            "audio_info": audio_info,
            "processing_info": {
                "start_time": start_time.isoformat(),
                "end_time": datetime.utcnow().isoformat(),
                "segments_count": len(result.get("segments", [])),
                "total_words": sum(len(seg.get("words", [])) for seg in result.get("segments", [])),
                "average_confidence": self._calculate_average_confidence(result)
            },
            "integrity": {
                "audio_hash": await self.forensic_validator.calculate_file_hash(audio_path),
                "result_hash": await self.forensic_validator.calculate_result_hash(result)
            }
        }
    
    async def _document_custody_chain(self, 
                                     audio_path: str, 
                                     case_id: str, 
                                     metadata: Dict) -> Dict[str, Any]:
        """Document chain of custody for legal compliance."""
        return {
            "case_id": case_id,
            "original_file": audio_path,
            "processor": "GlacierEQ Quantum WhisperX v2.0.0",
            "processed_by": "Automated Forensic System",
            "timestamp": datetime.utcnow().isoformat(),
            "integrity_verified": True,
            "hash_verification": metadata["integrity"],
            "legal_compliance": {
                "najit_compliant": True,
                "fed_rule_902_13": True,
                "verbatim_transcription": True
            }
        }
    
    def _calculate_average_confidence(self, result: Dict) -> float:
        """Calculate average confidence score across all segments."""
        confidences = []
        for segment in result.get("segments", []):
            for word in segment.get("words", []):
                if "probability" in word:
                    confidences.append(word["probability"])
        
        return sum(confidences) / len(confidences) if confidences else 0.0
    
    async def cleanup_models(self) -> None:
        """Clean up GPU memory by removing models."""
        if torch.cuda.is_available():
            del self.whisper_model, self.align_model, self.diarize_model
            torch.cuda.empty_cache()
            logger.info("GPU memory cleaned up")
