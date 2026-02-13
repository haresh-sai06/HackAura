import re
import logging
from typing import List
from models.emergency_schema import SeverityLevel, SeverityResult, EmergencyType

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
    
    def calculate_severity(self, transcript: str, emergency_type: EmergencyType) -> SeverityResult:
        """
        Calculate severity level based on transcript content and emergency type
        
        Args:
            transcript: Transcribed emergency call text
            emergency_type: Type of emergency
            
        Returns:
            SeverityResult with level, score, and risk indicators
        """
        logger.debug(f"⚡ SEVERITY ENGINE STARTING")
        logger.debug(f"   Input Transcript: '{transcript}'")
        logger.debug(f"   Emergency Type: {emergency_type.value}")
        
        transcript_lower = transcript.lower()
        severity_score = 0
        risk_indicators = []
        
        logger.debug(f"   🔍 CHECKING SEVERITY KEYWORDS:")
        
        # Check for severity indicators using the rules dictionary
        for indicator, points in self.severity_rules.items():
            if indicator in transcript_lower:
                severity_score += points
                risk_indicators.append(indicator)
                
                # Categorize severity level for logging
                if points >= 70:
                    logger.debug(f"      🚨 CRITICAL: Found '{indicator}' (+{points})")
                elif points >= 40:
                    logger.debug(f"      ⚠️  HIGH: Found '{indicator}' (+{points})")
                elif points >= 20:
                    logger.debug(f"      📋 MODERATE: Found '{indicator}' (+{points})")
                else:
                    logger.debug(f"      ℹ️  LOW: Found '{indicator}' (+{points})")
        
        # Apply emergency type multipliers
        type_multipliers = {
            EmergencyType.MEDICAL: 1.2,
            EmergencyType.FIRE: 1.3,
            EmergencyType.POLICE: 1.1,
            EmergencyType.ACCIDENT: 1.15,
            EmergencyType.MENTAL_HEALTH: 1.0,
            EmergencyType.OTHER: 0.8
        }
        
        multiplier = type_multipliers.get(emergency_type, 1.0)
        final_score = severity_score * multiplier
        
        logger.debug(f"   📊 SEVERITY CALCULATION:")
        logger.debug(f"      Base Score: {severity_score}")
        logger.debug(f"      Type Multiplier: {multiplier} ({emergency_type.value})")
        logger.debug(f"      Final Score: {final_score:.1f}")
        logger.debug(f"      Risk Indicators Found: {len(risk_indicators)}")
        logger.debug(f"      Risk Indicators: {risk_indicators}")
        
        # Determine severity level
        if final_score >= 80:
            level = SeverityLevel.LEVEL_1
            level_name = "Level 1 - Critical"
        elif final_score >= 60:
            level = SeverityLevel.LEVEL_2
            level_name = "Level 2 - High"
        elif final_score >= 40:
            level = SeverityLevel.LEVEL_3
            level_name = "Level 3 - Moderate"
        else:
            level = SeverityLevel.LEVEL_4
            level_name = "Level 4 - Low"
        
        logger.debug(f"   🎯 SEVERITY LEVEL DETERMINED:")
        logger.debug(f"      Score: {final_score:.1f}")
        logger.debug(f"      Level: {level_name}")
        logger.debug(f"      Thresholds: ≥80=Critical, ≥60=High, ≥40=Moderate, <40=Low")
        
        result = SeverityResult(
            level=level,
            score=min(final_score, 100),  # Cap at 100
            risk_indicators=risk_indicators
        )
        
        logger.info(f"⚡ SEVERITY COMPLETE: {level_name} (score: {final_score:.1f})")
        return result
    
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
