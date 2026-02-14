import logging
import time
from typing import Optional
from models.emergency_schema import (
    TriageResult, EmergencyType, SeverityLevel, EmergencyService
)
from services.ollama_triage_service import ollama_triage_service

logger = logging.getLogger(__name__)


class TriageEngine:
    def __init__(self):
        """Initialize Triage Engine with Ollama-based processing"""
        self.ollama_service = ollama_triage_service
        # Processing time tracking
        self.processing_times = []
        logger.info("🤖 TriageEngine initialized with Ollama-based processing (RAPID-100 Model)")
    
    async def process(self, transcript: str) -> TriageResult:
        """
        Main triage processing pipeline using Ollama AI model
        Unified single-step inference instead of multi-step rule-based pipeline
        
        Args:
            transcript: Transcribed emergency call text
            
        Returns:
            Complete TriageResult with all analysis
        """
        start_time = time.time()
        
        try:
            logger.info(f"🚀 Processing emergency transcript with Ollama...")
            logger.debug(f"   Input: {transcript[:100]}...")
            
            # Single unified call to Ollama AI for complete triage
            # Replaces: classification + severity + routing + summary in ONE call
            triage_result = await self.ollama_service.process(transcript)
            
            # Track processing time
            processing_time = triage_result.processing_time_ms
            self.processing_times.append(processing_time)
            
            # Log results
            logger.info(f"✅ Triage Results:")
            logger.info(f"   📍 Type: {triage_result.emergency_type.value}")
            logger.info(f"   🔴 Severity: {triage_result.severity_level.value} (Score: {triage_result.severity_score})")
            logger.info(f"   🏥 Service: {triage_result.assigned_service.value}")
            logger.info(f"   ⚡ Priority: {triage_result.priority}/10")
            logger.info(f"   🎯 Confidence: {triage_result.confidence:.2%}")
            logger.info(f"   ⏱️  Processing: {processing_time:.2f}ms")
            logger.info(f"   📝 Summary: {triage_result.summary}")
            
            return triage_result
            
        except Exception as e:
            logger.error(f"❌ Ollama triage processing failed: {e}")
            logger.error(f"   Exception: {type(e).__name__}")
            import traceback
            logger.debug(traceback.format_exc())
            
            # Return safe error result
            processing_time = (time.time() - start_time) * 1000
            return TriageResult(
                transcript=transcript,
                emergency_type=EmergencyType.MEDICAL,
                severity_level=SeverityLevel.LEVEL_2,
                severity_score=60.0,
                risk_indicators=["system_error", "manual_review_required"],
                assigned_service=EmergencyService.AMBULANCE,
                priority=8,
                summary="System error - escalating to manual review",
                confidence=0.3,
                processing_time_ms=processing_time
            )

    
    def get_processing_stats(self) -> dict:
        """
        Get processing statistics from Ollama service
        
        Returns:
            Dictionary with processing statistics
        """
        stats = self.ollama_service.get_stats()
        return {
            "engine": "Ollama AI (RAPID-100)",
            "total_processed": stats['total_calls'],
            "average_time_ms": stats['avg_ms'],
            "min_time_ms": stats['min_ms'],
            "max_time_ms": stats['max_ms'],
            "model_name": self.ollama_service.model_name,
            "performance_summary": f"{stats['avg_ms']:.2f}ms average latency"
        }
    
    def validate_triage_result(self, result: TriageResult) -> bool:
        """
        Validate triage result for consistency and accuracy
        
        Args:
            result: TriageResult to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Basic validation checks
        if not result.transcript:
            logger.warning("Empty transcript in triage result")
            return False
        
        if result.confidence < 0.3:
            logger.warning(f"Low confidence in triage result: {result.confidence}")
        
        if result.severity_score < 0 or result.severity_score > 100:
            logger.warning(f"Invalid severity score: {result.severity_score}")
            return False
        
        # Check severity level matches score ranges
        if result.severity_level == SeverityLevel.LEVEL_1 and result.severity_score < 80:
            logger.warning(f"LEVEL_1 severity but score {result.severity_score} < 80")
        
        return True


# Global instance
triage_engine = TriageEngine()
