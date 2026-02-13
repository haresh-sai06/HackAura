import re
import logging
from typing import Dict, List, Optional
from models.emergency_schema import EmergencyType, SeverityLevel, EmergencyService

logger = logging.getLogger(__name__)


class SummaryEngine:
    def __init__(self):
        # Common patterns for extracting key information
        self.location_patterns = [
            r'at\s+([A-Z][a-z]+\s+(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd))',
            r'on\s+([A-Z][a-z]+\s+(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd))',
            r'(\d+\s+[A-Z][a-z]+\s+(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd))',
            r'([A-Z][a-z]+\s+(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd))',
            r'(MG\s+Road| Brigade\s+Road| Commercial\s+Street| Residency\s+Road)',
            r'([A-Z][a-z]+\s+Area|[A-Z][a-z]+\s+Nagar|[A-Z][a-z]+\s+Colony)',
        ]
        
        self.victim_patterns = [
            r'(\d+[-\s]?year\s+old\s+(?:male|female|man|woman|boy|girl))',
            r'((?:male|female|man|woman|boy|girl),?\s+\d+)',
            r'(my\s+(?:father|mother|son|daughter|husband|wife|brother|sister))',
            r'((?:pregnant|elderly|child|baby))',
        ]
        
        self.time_patterns = [
            r'(\d+\s+(?:minutes|hours)\s+ago)',
            r'(just\s+now|recently|earlier)',
            r'(this\s+morning|this\s+afternoon|tonight|last\s+night)',
        ]
    
    def generate(self, transcript: str, emergency_type: EmergencyType, 
                 severity_level: SeverityLevel, risk_indicators: List[str]) -> str:
        """
        Generate dispatcher-ready summary from transcript and analysis
        
        Args:
            transcript: Original transcribed text
            emergency_type: Classified emergency type
            severity_level: Determined severity level
            risk_indicators: List of detected risk indicators
            
        Returns:
            Concise, operational summary for dispatchers
        """
        logger.debug(f"📝 SUMMARY ENGINE STARTING")
        logger.debug(f"   Input Transcript: '{transcript}'")
        logger.debug(f"   Emergency Type: {emergency_type.value}")
        logger.debug(f"   Severity Level: {severity_level.value}")
        logger.debug(f"   Risk Indicators: {risk_indicators}")
        
        try:
            logger.info(f"Generating summary for {emergency_type.value} emergency")
            
            # Extract key information
            victim_count = self._extract_victim_count(transcript)
            location = self._extract_location(transcript)
            time_info = self._extract_time_info(transcript)
            key_details = self._extract_key_details(transcript, risk_indicators)
            
            logger.debug(f"   🔍 INFORMATION EXTRACTION:")
            logger.debug(f"      Victim Count: {victim_count}")
            logger.debug(f"      Location: '{location}'")
            logger.debug(f"      Time Info: '{time_info}'")
            logger.debug(f"      Key Details: '{key_details}'")
            
            # Build summary parts
            summary_parts = []
            
            # Emergency type and severity
            severity_desc = self._get_severity_description(severity_level)
            summary_parts.append(f"{severity_desc} {emergency_type.value} emergency")
            logger.debug(f"      Base Summary: '{severity_desc} {emergency_type.value} emergency'")
            
            # Victim information
            if victim_count:
                victim_text = f"Victim(s): {victim_count}"
                summary_parts.append(victim_text)
                logger.debug(f"      Added Victim Info: '{victim_text}'")
            
            # Key details
            if key_details:
                summary_parts.append(f"Details: {key_details}")
                logger.debug(f"      Added Details: 'Details: {key_details}'")
            
            # Location if available
            if location:
                summary_parts.append(f"Location: {location}")
                logger.debug(f"      Added Location: 'Location: {location}'")
            
            # Time information if available
            if time_info:
                summary_parts.append(f"Time: {time_info}")
                logger.debug(f"      Added Time: 'Time: {time_info}'")
            
            # Add action required based on emergency type
            action_required = self._get_action_required(emergency_type, severity_level)
            summary_parts.append(f"Action: {action_required}")
            logger.debug(f"      Added Action: 'Action: {action_required}'")
            
            # Combine into final summary
            summary = ". ".join(summary_parts) + "."
            
            logger.debug(f"   📋 SUMMARY CONSTRUCTION:")
            logger.debug(f"      Summary Parts: {summary_parts}")
            logger.debug(f"      Raw Summary: '{summary}'")
            logger.debug(f"      Summary Length: {len(summary)} characters")
            
            # Ensure summary is concise (max 200 characters for dispatcher readability)
            if len(summary) > 200:
                original_summary = summary
                summary = self._truncate_summary(summary)
                logger.debug(f"      Summary Truncated: '{original_summary}' -> '{summary}'")
            
            logger.debug(f"   🎯 FINAL SUMMARY:")
            logger.debug(f"      Final Summary: '{summary}'")
            logger.debug(f"      Final Length: {len(summary)} characters")
            
            logger.info(f"📝 SUMMARY COMPLETE: '{summary}'")
            return summary
            
        except Exception as e:
            logger.error(f"❌ SUMMARY GENERATION FAILED: {e}")
            logger.error(f"🔍 ERROR DETAILS:")
            logger.error(f"   Transcript: '{transcript}'")
            logger.error(f"   Emergency Type: {emergency_type.value}")
            logger.error(f"   Severity Level: {severity_level.value}")
            logger.error(f"   Risk Indicators: {risk_indicators}")
            # Return basic summary on error
            fallback_summary = f"{emergency_type.value} emergency detected. {severity_level.value} severity. Immediate response required."
            logger.warning(f"📝 FALLBACK SUMMARY: '{fallback_summary}'")
            return fallback_summary
    
    def _extract_location(self, transcript: str) -> Optional[str]:
        """Extract location information from transcript"""
        for pattern in self.location_patterns:
            match = re.search(pattern, transcript, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    
    def _extract_victim_info(self, transcript: str) -> Optional[str]:
        """Extract victim information from transcript"""
        for pattern in self.victim_patterns:
            match = re.search(pattern, transcript, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    
    def _extract_time_info(self, transcript: str) -> Optional[str]:
        """Extract time information from transcript"""
        for pattern in self.time_patterns:
            match = re.search(pattern, transcript, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    
    def _extract_key_details(self, transcript: str, risk_indicators: List[str]) -> str:
        """Extract key incident details from risk indicators and transcript"""
        # Use the highest scoring risk indicators
        if not risk_indicators:
            return "Emergency reported"
        
        # Prioritize critical indicators
        critical_indicators = ['not breathing', 'gunshot', 'unconscious', 'fire spreading', 'heart attack']
        for indicator in critical_indicators:
            if indicator in risk_indicators:
                return indicator.replace('_', ' ').title()
        
        # Use first few indicators
        key_indicators = risk_indicators[:3]
        return ", ".join([ind.replace('_', ' ').title() for ind in key_indicators])
    
    def _get_severity_description(self, severity_level: SeverityLevel) -> str:
        """Get severity description for summary"""
        descriptions = {
            SeverityLevel.LEVEL_1: "Critical",
            SeverityLevel.LEVEL_2: "High-severity",
            SeverityLevel.LEVEL_3: "Moderate",
            SeverityLevel.LEVEL_4: "Low-severity"
        }
        return descriptions.get(severity_level, "Unknown")
    
    def _get_action_required(self, emergency_type: EmergencyType, severity_level: SeverityLevel) -> str:
        """Get action required based on emergency type and severity"""
        if severity_level == SeverityLevel.LEVEL_1:
            return "Immediate dispatch required"
        elif severity_level == SeverityLevel.LEVEL_2:
            return "Urgent dispatch required"
        else:
            return "Prompt dispatch required"
    
    def _truncate_summary(self, summary: str) -> str:
        """Truncate summary to maximum length while preserving key information"""
        # Try to truncate at sentence boundary
        sentences = summary.split('. ')
        truncated = ""
        
        for sentence in sentences:
            if len(truncated) + len(sentence) + 2 <= 200:
                truncated += sentence + ". "
            else:
                break
        
        if not truncated:
            # Fallback: hard truncate
            return summary[:197] + "..."
        
        return truncated.strip()


# Global instance
summary_engine = SummaryEngine()
