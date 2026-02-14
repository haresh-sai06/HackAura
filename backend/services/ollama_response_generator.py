"""
Enhanced Ollama Response Generator for Voice Interaction
Generates safety precautions, guidance, and voice-friendly responses
"""

import ollama
import json
import logging
from typing import Dict, Optional
from models.emergency_schema import TriageResult, SeverityLevel, EmergencyType

logger = logging.getLogger(__name__)


class OllamaResponseGenerator:
    def __init__(self, model_name: str = "qwen2.5:latest"):
        """Initialize response generator"""
        self.model_name = model_name
        logger.info(f"🎤 Ollama Response Generator initialized with model: {model_name}")
    
    def generate_voice_response(self, triage_result: TriageResult) -> Dict:
        """
        Generate comprehensive voice response with safety precautions
        
        Args:
            triage_result: Complete triage analysis from Ollama
            
        Returns:
            Dictionary with response text and precautions
        """
        try:
            # Build prompt for voice response generation
            prompt = self._build_voice_response_prompt(triage_result)
            
            logger.debug(f"📝 Generating voice response for {triage_result.emergency_type.value}")
            
            # Call Ollama for voice response
            response = ollama.chat(
                model=self.model_name,
                format='json',
                messages=[{'role': 'user', 'content': prompt}],
                stream=False
            )
            
            response_text = response['message']['content']
            response_data = json.loads(response_text)
            
            logger.debug(f"✅ Voice response generated")
            
            return {
                "voice_response": response_data.get('voice_response', ''),
                "safety_precautions": response_data.get('safety_precautions', []),
                "immediate_actions": response_data.get('immediate_actions', []),
                "caller_guidance": response_data.get('caller_guidance', ''),
                "dispatcher_summary": response_data.get('dispatcher_summary', ''),
                "is_life_threatening": triage_result.severity_level in [SeverityLevel.LEVEL_1, SeverityLevel.LEVEL_2]
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating voice response: {e}")
            return self._get_default_voice_response(triage_result)
    
    def _build_voice_response_prompt(self, triage_result: TriageResult) -> str:
        """
        Build prompt for voice response generation
        
        Args:
            triage_result: Triage analysis
            
        Returns:
            Formatted prompt for Ollama
        """
        emergency_type = triage_result.emergency_type.value
        severity = triage_result.severity_level.value
        risk_factors = ", ".join(triage_result.risk_indicators[:3])
        
        prompt = f"""You are a helpful emergency dispatcher. Generate a VOICE RESPONSE for a caller.

Emergency Details:
- Type: {emergency_type}
- Severity: {severity}
- Risk Factors: {risk_factors}
- Summary: {triage_result.summary}

Generate ONLY this JSON response (no other text):
{{
  "voice_response": "Calm, clear 1-2 sentence instruction to the caller. Speak naturally.",
  "safety_precautions": ["actionable precaution 1", "actionable precaution 2", "actionable precaution 3"],
  "immediate_actions": ["action 1 for caller to take now", "action 2"],
  "caller_guidance": "Reassuring statement about what to expect from responders",
  "dispatcher_summary": "Brief summary for emergency dispatcher"
}}

Guidelines:
1. Voice response should be calm, clear, and actionable (under 30 seconds to read)
2. Safety precautions must be specific and immediately doable
3. For LEVEL_1 (Critical): Emphasize urgency and evacuation/calling 911
4. For LEVEL_2 (High): Balance urgency with reassurance
5. For LEVEL_3/4: Reassuring tone, clear next steps
6. Avoid technical jargon
7. Be empathetic but directive"""
        
        return prompt
    
    def _get_default_voice_response(self, triage_result: TriageResult) -> Dict:
        """Get safe default response if Ollama fails"""
        
        is_critical = triage_result.severity_level in [SeverityLevel.LEVEL_1, SeverityLevel.LEVEL_2]
        
        default_responses = {
            "FIRE": {
                "voice_response": "Evacuate the building immediately and go to a safe location. Emergency services are on the way.",
                "safety_precautions": [
                    "Leave the building immediately",
                    "Do not use elevators",
                    "Close doors behind you to contain smoke",
                    "Move to designated assembly point"
                ],
                "immediate_actions": [
                    "Evacuate now",
                    "Call out for others to evacuate",
                    "Move away from the building"
                ]
            },
            "POLICE": {
                "voice_response": "Stay in a safe location if possible. Police are being dispatched to your location immediately.",
                "safety_precautions": [
                    "Move to a safe, secure location",
                    "Keep doors locked",
                    "Do not confront the person",
                    "Observe and remember details for police"
                ],
                "immediate_actions": [
                    "Move to safety",
                    "Lock doors",
                    "Stay on the line with dispatcher"
                ]
            },
            "ACCIDENT": {
                "voice_response": "Please move to a safe location away from traffic if possible. Emergency services are responding.",
                "safety_precautions": [
                    "Move to a safe location away from traffic",
                    "Turn on hazard lights if in vehicle",
                    "Do not move injured persons unless in immediate danger",
                    "Cover injured persons if possible"
                ],
                "immediate_actions": [
                    "Move to safety",
                    "Turn on hazard lights",
                    "Stay with the caller"
                ]
            },
            "MENTAL_HEALTH": {
                "voice_response": "We understand this is difficult. Help is on the way. Please stay on the line with us.",
                "safety_precautions": [
                    "Move to a safe, calm location",
                    "Remove any potentially harmful items if safe to do so",
                    "Keep company with trusted person if possible",
                    "Continue to breathe slowly and steadily"
                ],
                "immediate_actions": [
                    "Stay on the line",
                    "Move to a safe space",
                    "Ask for support from someone nearby"
                ]
            }
        }
        
        emergency_type = triage_result.emergency_type.value
        default = default_responses.get(emergency_type, {
            "voice_response": "Help is on the way. Please stay on the line with us.",
            "safety_precautions": ["Stay calm", "Stay on the line", "Follow dispatcher instructions"],
            "immediate_actions": ["Stay safe", "Stay on the line"]
        })
        
        return {
            "voice_response": default.get("voice_response", ""),
            "safety_precautions": default.get("safety_precautions", []),
            "immediate_actions": default.get("immediate_actions", []),
            "caller_guidance": "Emergency services are being deployed to your location immediately.",
            "dispatcher_summary": f"{emergency_type} emergency - {triage_result.severity_level.value}",
            "is_life_threatening": is_critical
        }


# Create singleton instance
ollama_response_generator = OllamaResponseGenerator()
