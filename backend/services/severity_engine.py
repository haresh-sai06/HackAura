import re
import logging
from typing import List, Tuple
from models.emergency_schema import SeverityLevel, SeverityResult

logger = logging.getLogger(__name__)


class SeverityEngine:
    def __init__(self):
        # Define severity scoring rules (deterministic, rule-based)
        self.severity_rules = {
            # Critical indicators (80+ points)
            'not breathing': 80,
            'stopped breathing': 80,
            'can\'t breathe': 75,
            'difficulty breathing': 60,
            'gunshot': 70,
            'shooting': 70,
            'shot': 65,
            'unconscious': 60,
            'passed out': 55,
            'collapsed': 50,
            'bleeding heavily': 50,
            'severe bleeding': 50,
            'massive bleeding': 55,
            'fire spreading': 80,
            'building on fire': 75,
            'explosion': 70,
            'exploded': 65,
            'heart attack': 65,
            'cardiac arrest': 80,
            'stroke': 60,
            'seizure': 45,
            
            # High severity indicators (40-60 points)
            'accident': 40,
            'car crash': 50,
            'collision': 45,
            'broken bone': 35,
            'fracture': 35,
            'head injury': 45,
            'serious injury': 40,
            'major injury': 45,
            'multiple injuries': 50,
            'trapped': 55,
            'stuck': 40,
            'fall from height': 50,
            
            # Moderate severity indicators (20-40 points)
            'bleeding': 25,
            'cut': 20,
            'wound': 25,
            'burn': 30,
            'pain': 20,
            'hurt': 20,
            'injured': 25,
            'fall': 25,
            'slipped': 20,
            'tripped': 20,
            
            # Panic indicators (20 points)
            'help': 20,
            'emergency': 25,
            'urgent': 20,
            'quickly': 15,
            'fast': 15,
            'immediately': 20,
            'right away': 15,
            'please help': 25,
            'someone help': 25,
            
            # Mental health crisis indicators (40 points)
            'suicide': 60,
            'kill myself': 65,
                'self harm': 50,
            'depressed': 30,
            'panic attack': 35,
            'mental health': 25,
            'crisis': 35,
            'breakdown': 30,
            'overwhelmed': 25,
        }
        
        # Severity level mapping
        self.severity_thresholds = {
            SeverityLevel.LEVEL_1: 80,  # Critical
            SeverityLevel.LEVEL_2: 60,  # High
            SeverityLevel.LEVEL_3: 40,  # Moderate
            SeverityLevel.LEVEL_4: 0    # Low (everything below 40)
        }
    
    def calculate(self, transcript: str) -> SeverityResult:
        """
        Calculate severity score based on deterministic rules
        
        Args:
            transcript: Transcribed emergency call text
            
        Returns:
            SeverityResult with level, score, and risk indicators
        """
        try:
            logger.info(f"Calculating severity for transcript: {transcript[:100]}...")
            
            # Normalize text
            normalized_text = transcript.lower()
            
            # Calculate total severity score
            total_score = 0
            risk_indicators = []
            matched_rules = []
            
            for keyword, score in self.severity_rules.items():
                # Find all occurrences of the keyword
                pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
                matches = pattern.findall(normalized_text)
                
                if matches:
                    count = len(matches)
                    keyword_score = score * count
                    total_score += keyword_score
                    
                    # Add to risk indicators
                    risk_indicators.extend([keyword] * count)
                    matched_rules.append(f"{keyword}: +{keyword_score} (x{count})")
            
            # Cap score at 100
            total_score = min(total_score, 100)
            
            # Determine severity level
            severity_level = self._determine_level(total_score)
            
            # Remove duplicate risk indicators while preserving order
            unique_risk_indicators = list(dict.fromkeys(risk_indicators))
            
            result = SeverityResult(
                level=severity_level,
                score=total_score,
                risk_indicators=unique_risk_indicators
            )
            
            logger.info(f"Severity calculation: {total_score} -> {severity_level.value}")
            logger.debug(f"Matched rules: {matched_rules}")
            logger.debug(f"Risk indicators: {unique_risk_indicators}")
            
            return result
            
        except Exception as e:
            logger.error(f"Severity calculation failed: {e}")
            # Return default severity on error
            return SeverityResult(
                level=SeverityLevel.LEVEL_3,
                score=30.0,
                risk_indicators=["system_error"]
            )
    
    def _determine_level(self, score: float) -> SeverityLevel:
        """
        Determine severity level based on score
        
        Args:
            score: Calculated severity score
            
        Returns:
            SeverityLevel enum value
        """
        for level, threshold in self.severity_thresholds.items():
            if score >= threshold:
                return level
        
        return SeverityLevel.LEVEL_4
    
    def get_explanation(self, result: SeverityResult) -> str:
        """
        Generate human-readable explanation for severity calculation
        
        Args:
            result: SeverityResult to explain
            
        Returns:
            Explanation string
        """
        explanation = f"Severity Score: {result.score}/100\n"
        explanation += f"Level: {result.level.value}\n"
        explanation += f"Risk Indicators: {', '.join(result.risk_indicators)}\n"
        
        # Add threshold explanation
        if result.score >= 80:
            explanation += "Critical severity detected - immediate response required"
        elif result.score >= 60:
            explanation += "High severity - urgent response required"
        elif result.score >= 40:
            explanation += "Moderate severity - prompt response required"
        else:
            explanation += "Low severity - standard response"
        
        return explanation


# Global instance
severity_engine = SeverityEngine()
