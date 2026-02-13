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
            severity_level: Calculated severity level
            risk_indicators: List of detected risk indicators
            
        Returns:
            Concise, operational summary for dispatchers
        """
        try:
            logger.info(f"Generating summary for {emergency_type.value} emergency")
            
            # Extract key information
            location = self._extract_location(transcript)
            victim_info = self._extract_victim_info(transcript)
            time_info = self._extract_time_info(transcript)
            
            # Build summary components
            summary_parts = []
            
            # Start with emergency type and severity
            severity_desc = self._get_severity_description(severity_level)
            summary_parts.append(f"{severity_desc} {emergency_type.value} emergency")
            
            # Add victim information if available
            if victim_info:
                summary_parts.append(f"Victim: {victim_info}")
            
            # Add key symptoms/incident details
            key_details = self._extract_key_details(transcript, risk_indicators)
            if key_details:
                summary_parts.append(f"Details: {key_details}")
            
            # Add location if available
            if location:
                summary_parts.append(f"Location: {location}")
            
            # Add time information if available
            if time_info:
                summary_parts.append(f"Time: {time_info}")
            
            # Add action required based on emergency type
            action_required = self._get_action_required(emergency_type, severity_level)
            summary_parts.append(f"Action: {action_required}")
            
            # Combine into final summary
            summary = ". ".join(summary_parts) + "."
            
            # Ensure summary is concise (max 200 characters for dispatcher readability)
            if len(summary) > 200:
                summary = self._truncate_summary(summary)
            
            logger.info(f"Generated summary: {summary}")
            return summary
            
        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            # Return basic summary on error
            return f"{emergency_type.value} emergency detected. {severity_level.value} severity. Immediate response required."
    
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
