import logging
import time
from typing import Optional
from models.emergency_schema import (
    TriageResult, ClassificationResult, SeverityResult, 
    RoutingResult, EmergencyType, SeverityLevel, EmergencyService
)
from services.classification_engine import classification_engine
from services.severity_engine import severity_engine
from services.routing_engine import routing_engine
from services.summary_engine import summary_engine

logger = logging.getLogger(__name__)


class TriageEngine:
    def __init__(self):
        self.classification_engine = classification_engine
        self.severity_engine = severity_engine
        self.routing_engine = routing_engine
        self.summary_engine = summary_engine
        
        # Processing time tracking
        self.processing_times = []
    
    async def process(self, transcript: str) -> TriageResult:
        """
        Main triage processing pipeline
        
        Args:
            transcript: Transcribed emergency call text
            
        Returns:
            Complete TriageResult with all analysis
        """
        start_time = time.time()
        
        try:
            logger.info(f"Starting triage processing for transcript: {transcript[:100]}...")
            
            # Step 1: Classification
            logger.info("Step 1: Classification")
            classification_result = self.classification_engine.classify(transcript)
            logger.info(f"Classification: {classification_result.emergency_type.value} (confidence: {classification_result.confidence:.2f})")
            
            # Step 2: Severity Assessment
            logger.info("Step 2: Severity Assessment")
            severity_result = self.severity_engine.calculate(transcript)
            logger.info(f"Severity: {severity_result.level.value} (score: {severity_result.score})")
            
            # Step 3: Routing
            logger.info("Step 3: Routing")
            routing_result = self.routing_engine.route(
                classification_result.emergency_type, 
                severity_result.level
            )
            logger.info(f"Routing: {routing_result.assigned_service.value} (priority: {routing_result.priority})")
            
            # Step 4: Summary Generation
            logger.info("Step 4: Summary Generation")
            summary = self.summary_engine.generate(
                transcript,
                classification_result.emergency_type,
                severity_result.level,
                severity_result.risk_indicators
            )
            logger.info(f"Summary: {summary[:100]}...")
            
            # Calculate processing time
            processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            self.processing_times.append(processing_time)
            
            # Calculate overall confidence (weighted average)
            overall_confidence = self._calculate_overall_confidence(
                classification_result.confidence,
                severity_result.score
            )
            
            # Create final triage result
            triage_result = TriageResult(
                transcript=transcript,
                emergency_type=classification_result.emergency_type,
                severity_level=severity_result.level,
                severity_score=severity_result.score,
                risk_indicators=severity_result.risk_indicators,
                assigned_service=routing_result.assigned_service,
                priority=routing_result.priority,
                location=self._extract_location(transcript),
                summary=summary_result.summary,
                confidence=overall_confidence,
                processing_time_ms=processing_time
            )
            
            logger.info(f"Triage completed in {processing_time:.2f}ms")
            self._log_triage_result(triage_result)
            
            return triage_result
            
        except Exception as e:
            logger.error(f"Triage processing failed: {e}")
            # Return error result
            processing_time = (time.time() - start_time) * 1000
            return TriageResult(
                transcript=transcript,
                emergency_type=EmergencyType.MEDICAL,
                severity_level=SeverityLevel.LEVEL_3,
                severity_score=30.0,
                risk_indicators=["system_error"],
                assigned_service=EmergencyService.AMBULANCE,
                priority=5,  # Added priority field
                summary="System error during triage. Default medical response initiated.",
                confidence=0.3,
                processing_time_ms=processing_time
            )
    
    def _calculate_overall_confidence(self, classification_confidence: float, severity_score: float) -> float:
        """
        Calculate overall confidence from classification confidence and severity score
        
        Args:
            classification_confidence: Confidence from classification engine (0-1)
            severity_score: Severity score from severity engine (0-100)
            
        Returns:
            Overall confidence score (0-1)
        """
        # Normalize severity score to 0-1 range
        normalized_severity = min(severity_score / 100, 1.0)
        
        # Weight classification more heavily than severity
        overall_confidence = (classification_confidence * 0.7) + (normalized_severity * 0.3)
        
        return min(overall_confidence, 1.0)
    
    def _extract_location(self, transcript: str) -> Optional[str]:
        """
        Extract location information from transcript
        
        Args:
            transcript: Emergency call transcript
            
        Returns:
            Location string if found, None otherwise
        """
        import re
        
        # Common location patterns in Bangalore
        location_patterns = [
            r'\b(MG Road|MG Road|M G Road)\b',
            r'\b(Brigade Road|Brigade Rd)\b',
            r'\b(Commercial Street|Commercial St)\b',
            r'\b(Indiranagar|Indira Nagar)\b',
            r'\b(Koramangala|Koramangala)\b',
            r'\b(Whitefield|White Field)\b',
            r'\b(Electronic City|Electronic City)\b',
            r'\b(HSR Layout|HSR)\b',
            r'\b(Jayanagar|Jaya Nagar)\b',
            r'\b(BTM Layout|BTM)\b'
        ]
        
        transcript_lower = transcript.lower()
        
        for pattern in location_patterns:
            match = re.search(pattern, transcript_lower, re.IGNORECASE)
            if match:
                return match.group(1).title()
        
        # Look for any road/street patterns
        road_match = re.search(r'\b(\w+(?:\s+\w+)*)\s+(road|rd|street|st|nagar|layout)\b', transcript_lower, re.IGNORECASE)
        if road_match:
            return road_match.group(1).title() + ' ' + road_match.group(2).title()
        
        return None
    
    def _log_triage_result(self, result: TriageResult) -> None:
        """
        Log triage result for audit and debugging
        
        Args:
            result: TriageResult to log
        """
        log_data = {
            "emergency_type": result.emergency_type.value,
            "severity_level": result.severity_level.value,
            "severity_score": result.severity_score,
            "assigned_service": result.assigned_service.value,
            "confidence": result.confidence,
            "processing_time_ms": result.processing_time_ms,
            "risk_indicators_count": len(result.risk_indicators),
            "summary_length": len(result.summary)
        }
        
        logger.info(f"Triage Result: {log_data}")
        
        # Log detailed risk indicators if any
        if result.risk_indicators:
            logger.debug(f"Risk Indicators: {result.risk_indicators}")
    
    def get_processing_stats(self) -> dict:
        """
        Get processing statistics
        
        Returns:
            Dictionary with processing statistics
        """
        if not self.processing_times:
            return {"message": "No processing data available"}
        
        avg_time = sum(self.processing_times) / len(self.processing_times)
        min_time = min(self.processing_times)
        max_time = max(self.processing_times)
        
        return {
            "total_processed": len(self.processing_times),
            "average_time_ms": avg_time,
            "min_time_ms": min_time,
            "max_time_ms": max_time,
            "under_5_seconds": sum(1 for t in self.processing_times if t < 5000),
            "performance_ratio": sum(1 for t in self.processing_times if t < 5000) / len(self.processing_times)
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
        
        # Check for logical consistency
        if result.severity_level == SeverityLevel.LEVEL_1 and result.assigned_service == EmergencyService.CRISIS_RESPONSE:
            logger.warning("Critical severity with crisis response - may need escalation")
        
        return True


# Global instance
triage_engine = TriageEngine()
