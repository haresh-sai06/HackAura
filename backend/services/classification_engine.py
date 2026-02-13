import re
import logging
from typing import Dict, List, Tuple
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
                'house fire', 'forest fire', 'arson', 'extinguisher', 'fire department'
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
        Classify emergency type based on transcript using keyword matching
        
        Args:
            transcript: Transcribed emergency call text
            
        Returns:
            ClassificationResult with emergency type and confidence
        """
        try:
            logger.info(f"Starting classification for transcript: {transcript[:100]}...")
            
            # Normalize text
            normalized_text = transcript.lower()
            
            # Calculate scores for each emergency type
            scores = {}
            for emergency_type, keywords in self.emergency_keywords.items():
                score = 0
                matched_keywords = []
                
                for keyword in keywords:
                    # Count occurrences of each keyword
                    pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
                    matches = pattern.findall(normalized_text)
                    if matches:
                        count = len(matches)
                        score += count
                        matched_keywords.extend([keyword] * count)
                
                scores[emergency_type] = {
                    'score': score,
                    'keywords': matched_keywords
                }
            
            # Find the best match
            best_type = None
            best_score = 0
            
            for emergency_type, data in scores.items():
                if data['score'] > best_score:
                    best_score = data['score']
                    best_type = emergency_type
            
            # Calculate confidence based on score and total keywords found
            total_keywords = sum(data['score'] for data in scores.values())
            
            if total_keywords == 0:
                # No keywords found, default to medical with low confidence
                confidence = 0.3
                emergency_type = EmergencyType.MEDICAL
                logger.warning("No emergency keywords detected, defaulting to medical")
            else:
                confidence = min(best_score / total_keywords, 1.0)
                emergency_type = best_type
            
            # Ensure minimum confidence threshold
            if confidence < 0.3:
                confidence = 0.3
            
            result = ClassificationResult(
                emergency_type=emergency_type,
                confidence=confidence
            )
            
            logger.info(f"Classification result: {emergency_type.value} with confidence {confidence:.2f}")
            return result
            
        except Exception as e:
            logger.error(f"Classification failed: {e}")
            # Return default classification on error
            return ClassificationResult(
                emergency_type=EmergencyType.MEDICAL,
                confidence=0.3
            )


# Global instance
classification_engine = ClassificationEngine()
