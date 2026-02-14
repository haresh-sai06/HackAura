"""
Ollama-based Emergency Call Triage Service
Replaces rule-based classification, severity, and routing engines with AI model
Optimized for low-latency, high-accuracy emergency response
"""

import ollama
import json
import logging
import time
import re
from typing import Optional
from models.emergency_schema import (
    EmergencyType, SeverityLevel, EmergencyService,
    ClassificationResult, SeverityResult, RoutingResult,
    TriageResult
)

logger = logging.getLogger(__name__)


class OllamaTriageService:
    def __init__(self, model_name: str = "qwen2.5:0.5b", temperature: float = 0.1):
        """
        Initialize Ollama Triage Service
        
        Args:
            model_name: Name of the Ollama model to use
            temperature: Temperature for model responses (lower = more deterministic)
        """
        self.model_name = model_name
        self.temperature = temperature
        self.processing_times = []
        
        logger.info(f"🤖 Ollama Triage Service initialized with model: {model_name}")
    
    async def process(self, transcript: str) -> TriageResult:
        """
        Process emergency transcript using Ollama model
        Combines classification, severity, routing, and summarization in one call
        
        Args:
            transcript: Transcribed emergency call text
            
        Returns:
            Complete TriageResult with all analysis
        """
        start_time = time.time()
        
        try:
            logger.info(f"🎯 Ollama processing started for transcript: {transcript[:50]}...")
            
            # Call Ollama with structured prompt
            prompt = self._build_triage_prompt(transcript)
            logger.debug(f"📝 Prompt sent to Ollama: {prompt[:100]}...")
            
            # Call Ollama model with optimized settings
            response = ollama.chat(
                model=self.model_name,
                format='json',
                messages=[{'role': 'user', 'content': prompt}],
                stream=False,
                options={
                    'temperature': self.temperature,
                    'num_ctx': 256,  # Reduced context for speed
                    'num_predict': 100,  # Limit output tokens
                    'top_k': 5,  # Reduced top_k for speed
                    'timeout': 3  # 3 second timeout
                }
            )
            
            # Extract and parse response
            response_text = response['message']['content']
            logger.debug(f"📥 Raw Ollama response: {response_text[:200]}...")
            
            # Parse JSON response
            triage_data = json.loads(response_text)
            logger.debug(f"✅ Parsed triage data: {json.dumps(triage_data, indent=2)[:300]}...")
            
            # Calculate processing time
            processing_time = (time.time() - start_time) * 1000  # milliseconds
            self.processing_times.append(processing_time)
            logger.info(f"⏱️  Triage processing completed in {processing_time:.2f}ms")
            
            # Build TriageResult from parsed data
            triage_result = self._build_triage_result(
                transcript=transcript,
                triage_data=triage_data,
                processing_time=processing_time
            )
            
            logger.info(f"✅ Final triage result ready")
            logger.info(f"   Type: {triage_result.emergency_type}")
            logger.info(f"   Severity: {triage_result.severity_level}")
            logger.info(f"   Service: {triage_result.assigned_service}")
            
            return triage_result
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parsing failed: {e}")
            return self._create_error_result(transcript, start_time, "JSON parsing error")
        except Exception as e:
            logger.error(f"❌ Ollama processing failed: {e}")
            logger.error(f"   Exception: {type(e).__name__}: {str(e)}")
            return self._create_error_result(transcript, start_time, str(e))
    
    def _build_triage_prompt(self, transcript: str) -> str:
        """
        Build ultra-minimal prompt for maximum speed
        
        Args:
            transcript: Emergency call transcript
            
        Returns:
            Formatted prompt for Ollama
        """
        prompt = f"""Analyze emergency and output JSON:

"{transcript}"

TYPES: MEDICAL,FIRE,POLICE,ACCIDENT,MENTAL_HEALTH,OTHER
SEVERITY: LEVEL_1(80-100),LEVEL_2(60-79),LEVEL_3(40-59),LEVEL_4(0-39)
SERVICES: AMBULANCE,FIRE_DEPARTMENT,POLICE,CRISIS_RESPONSE,MULTIPLE

JSON:
{{
  "emergency_type": "type",
  "severity_level": "level",
  "severity_score": 0-100,
  "confidence": 0.0-1.0,
  "assigned_service": "service",
  "priority": 1-10,
  "summary": "brief summary"
}}"""
        
        return prompt
    
    def _build_triage_result(
        self,
        transcript: str,
        triage_data: dict,
        processing_time: float
    ) -> TriageResult:
        """
        Build TriageResult from Ollama response data
        
        Args:
            transcript: Original emergency transcript
            triage_data: Parsed JSON response from Ollama
            processing_time: Processing time in milliseconds
            
        Returns:
            TriageResult object
        """
        try:
            # Map string values to enums with validation
            emergency_type = self._parse_enum(
                triage_data.get('emergency_type', 'MEDICAL'),
                EmergencyType,
                EmergencyType.MEDICAL
            )
            
            severity_level = self._parse_enum(
                triage_data.get('severity_level', 'LEVEL_3'),
                SeverityLevel,
                SeverityLevel.LEVEL_3
            )
            
            assigned_service = self._parse_enum(
                triage_data.get('assigned_service', 'AMBULANCE'),
                EmergencyService,
                EmergencyService.AMBULANCE
            )
            
            # Extract numerical values
            severity_score = float(triage_data.get('severity_score', 50.0))
            severity_score = max(0.0, min(100.0, severity_score))  # Clamp to 0-100
            
            confidence = float(triage_data.get('confidence', 0.7))
            confidence = max(0.0, min(1.0, confidence))  # Clamp to 0-1
            
            priority = int(triage_data.get('priority', 5))
            priority = max(1, min(10, priority))  # Clamp to 1-10
            
            # Extract other fields
            risk_indicators = triage_data.get('risk_indicators', [])
            if not isinstance(risk_indicators, list):
                risk_indicators = [risk_indicators]
            
            location = triage_data.get('location')
            if location and location.lower() == 'null':
                location = None
            
            summary = triage_data.get('summary', 'Emergency assistance required')
            
            # Create TriageResult
            result = TriageResult(
                transcript=transcript,
                emergency_type=emergency_type,
                severity_level=severity_level,
                severity_score=severity_score,
                risk_indicators=risk_indicators,
                assigned_service=assigned_service,
                priority=priority,
                location=location,
                summary=summary,
                confidence=confidence,
                processing_time_ms=processing_time
            )
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error building triage result: {e}")
            raise
    
    def _parse_enum(self, value: str, enum_class, default):
        """
        Safely parse enum value from string
        
        Args:
            value: String value to parse
            enum_class: Enum class to parse into
            default: Default value if parsing fails
            
        Returns:
            Parsed enum value or default
        """
        try:
            if isinstance(value, enum_class):
                return value
            
            # Try exact match first
            return enum_class(value.upper())
        except (ValueError, AttributeError):
            try:
                # Try case-insensitive match
                for member in enum_class:
                    if member.value.upper() == value.upper():
                        return member
            except:
                pass
            
            logger.warning(f"Could not parse enum value '{value}', using default: {default}")
            return default
    
    def _create_error_result(
        self,
        transcript: str,
        start_time: float,
        error_message: str
    ) -> TriageResult:
        """
        Create safe error result for failed processing
        
        Args:
            transcript: Original transcript
            start_time: Processing start time
            error_message: Error message
            
        Returns:
            Safe default TriageResult
        """
        processing_time = (time.time() - start_time) * 1000
        
        return TriageResult(
            transcript=transcript,
            emergency_type=EmergencyType.MEDICAL,
            severity_level=SeverityLevel.LEVEL_2,
            severity_score=60.0,
            risk_indicators=["system_error", "fallback_to_manual_review"],
            assigned_service=EmergencyService.AMBULANCE,
            priority=8,  # High priority for error cases
            location=None,
            summary="System error during triage. Manual review recommended.",
            confidence=0.3,
            processing_time_ms=processing_time
        )
    
    def get_average_processing_time(self) -> float:
        """
        Get average processing time in milliseconds
        
        Returns:
            Average processing time
        """
        if not self.processing_times:
            return 0.0
        return sum(self.processing_times) / len(self.processing_times)
    
    def get_stats(self) -> dict:
        """
        Get service statistics
        
        Returns:
            Dictionary with processing stats
        """
        if not self.processing_times:
            return {
                'total_calls': 0,
                'avg_ms': 0.0,
                'min_ms': 0.0,
                'max_ms': 0.0
            }
        
        return {
            'total_calls': len(self.processing_times),
            'avg_ms': sum(self.processing_times) / len(self.processing_times),
            'min_ms': min(self.processing_times),
            'max_ms': max(self.processing_times)
        }


# Create singleton instance
ollama_triage_service = OllamaTriageService()
