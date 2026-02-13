import re
import logging
from typing import List
from models.emergency_schema import EmergencyType, ClassificationResult

logger = logging.getLogger(__name__)


class ClassificationEngine:
    def __init__(self):
        # Define keyword patterns for each emergency type
        self.emergency_keywords = {
            EmergencyType.MEDICAL: [
                'heart attack', 'chest pain', 'stroke', 'unconscious', 'not breathing',
                'bleeding', 'blood', 'injury', 'hurt', 'pain', 'medical', 'ambulance',
                'hospital', 'doctor', 'nurse', 'medicine', 'drug', 'overdose', 'poison',
                'allergic reaction', 'seizure', 'fainting', 'collapsed', 'difficulty breathing',
                'shortness of breath', 'broken bone', 'fracture', 'wound', 'cut', 'burn'
            ],
            EmergencyType.FIRE: [
                'fire', 'burning', 'smoke', 'flames', 'explosion', 'caught fire',
                'on fire', 'smoking', 'electrical fire', 'gas leak', 'building on fire',
                'house fire', 'forest fire', 'arson', 'extinguisher', 'fire department',
                'fire accident', 'fire emergency'
            ],
            EmergencyType.POLICE: [
                'police', 'theft', 'stolen', 'robbery', 'burglar', 'break in', 'assault',
                'attack', 'fight', 'violence', 'weapon', 'gun', 'knife', 'shooting',
                'gunshot', 'threat', 'harassment', 'domestic violence', 'suspicious',
                'crime', 'criminal', 'intruder', 'stalker', 'kidnapping', 'missing person'
            ],
            EmergencyType.ACCIDENT: [
                'accident', 'crash', 'collision', 'car accident', 'traffic accident',
                'vehicle crash', 'hit and run', 'road accident', 'pileup', 'overturned',
                'fallen', 'slipped', 'tripped', 'industrial accident', 'workplace accident',
                'construction accident', 'building collapse'
            ],
            EmergencyType.MENTAL_HEALTH: [
                'suicide', 'kill myself', 'depressed', 'anxiety', 'panic attack',
                'mental health', 'crisis', 'breakdown', 'overwhelmed', 'can\'t cope',
                'self harm', 'depression', 'bipolar', 'schizophrenia', 'psychiatric',
                'counseling', 'therapy', 'mental crisis', 'emotional distress'
            ]
        }
        
    def classify(self, transcript: str) -> ClassificationResult:
        """
        Classify emergency type from transcript
        
        Args:
            transcript: Transcribed emergency call text
            
        Returns:
            ClassificationResult with emergency type and confidence
        """
        logger.debug(f"🔍 CLASSIFICATION ENGINE STARTING")
        logger.debug(f"   Input Transcript: '{transcript}'")
        logger.debug(f"   Transcript Length: {len(transcript)} characters")
        logger.debug(f"   Transcript Lower: '{transcript.lower()}'")
        
        # DEBUG: Print to console for immediate visibility
        print(f"🔍 CLASSIFICATION DEBUG: '{transcript.lower()}'")
        
        transcript_lower = transcript.lower()
        scores = {}
        
        # Calculate scores for each emergency type
        for emergency_type, keywords in self.emergency_keywords.items():
            score = 0
            matched_keywords = []
            
            logger.debug(f"   🏷️  Checking {emergency_type.upper()}:")
            
            for keyword in keywords:
                if keyword in transcript_lower:
                    # Count occurrences for weighted scoring
                    occurrences = transcript_lower.count(keyword)
                    keyword_score = len(keyword) * occurrences  # Weight by keyword length
                    score += keyword_score
                    matched_keywords.append(keyword)
                    logger.debug(f"      ✅ Found '{keyword}' (x{occurrences}) - Score: {keyword_score}")
                    print(f"✅ FOUND KEYWORD: '{keyword}' in '{transcript_lower}'")
                else:
                    logger.debug(f"      ❌ Missing '{keyword}'")
            
            scores[emergency_type] = score
            logger.debug(f"   📊 {emergency_type.upper()} Total Score: {score}")
            logger.debug(f"   🎯 Matched Keywords: {matched_keywords}")
            print(f"📊 {emergency_type.upper()} SCORE: {score}")
        
        # Find the emergency type with highest score
        best_type = max(scores, key=scores.get)
        best_score = scores[best_type]
        
        # Normalize score to 0-1 range
        max_possible_score = sum(len(k) for k in self.emergency_keywords[best_type])
        confidence = min(best_score / max_possible_score, 1.0) if max_possible_score > 0 else 0.0
        
        logger.debug(f"🏆 CLASSIFICATION RESULTS:")
        logger.debug(f"   🥇 Best Type: {best_type}")
        logger.debug(f"   📈 Best Score: {best_score}")
        logger.debug(f"   🎯 Max Possible Score: {max_possible_score}")
        logger.debug(f"   📊 Normalized Confidence: {confidence:.3f}")
        logger.debug(f"   📋 All Scores: {scores}")
        
        print(f"🏆 FINAL RESULT: {best_type} (confidence: {confidence:.2f})")
        
        result = ClassificationResult(
            emergency_type=EmergencyType(best_type),
            confidence=confidence
        )
        
        logger.info(f"✅ CLASSIFICATION COMPLETE: {best_type} (confidence: {confidence:.2f})")
        return result


# Global instance
classification_engine = ClassificationEngine()
