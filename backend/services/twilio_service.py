from twilio.twiml.voice_response import VoiceResponse, Gather, Record
from typing import Optional
from config import settings
from models.emergency_schema import TriageResult
from services.ollama_response_generator import ollama_response_generator
import logging

logger = logging.getLogger(__name__)

class TwilioService:
    def __init__(self):
        self.ai_voice = settings.AI_ASSISTANT_VOICE
    
    def generate_emergency_speech_response(self) -> str:
        """Generate emergency triage TwiML response using Twilio's free speech recognition"""
        response = VoiceResponse()
        
        # Create gather to capture user speech using Twilio's free speech recognition
        gather = Gather(
            input='speech',
            timeout=settings.SPEECH_TIMEOUT,
            action='/api/voice/process',
            method='POST',
            language='en-US',
            speech_timeout=5,  # Wait 5 seconds for speech
            speech_model='phone_call'  # Optimized for phone calls
        )
        
        emergency_message = "Emergency services. Please describe your emergency clearly and calmly."
        gather.say(emergency_message, voice=self.ai_voice, language='en-US')
        
        response.append(gather)
        
        # If no speech detected, try again
        response.say("I didn't catch that. Please state your emergency now.", voice=self.ai_voice, language='en-US')
        
        # Final fallback
        response.say("If you need immediate assistance, please call back. Goodbye.", voice=self.ai_voice, language='en-US')
        response.hangup()
        
        return str(response)
    
    def generate_emergency_retry_response(self) -> str:
        """Generate retry response for emergency input using speech recognition"""
        response = VoiceResponse()
        
        # Create gather to capture emergency description using speech recognition
        gather = Gather(
            input='speech',
            timeout=settings.SPEECH_TIMEOUT,
            action='/api/voice/process',
            method='POST',
            language='en-US',
            speech_timeout=5,
            speech_model='phone_call'
        )
        
        retry_message = "Please describe your emergency. What services do you need?"
        gather.say(retry_message, voice=self.ai_voice, language='en-US')
        
        response.append(gather)
        
        # Final fallback
        response.say("Emergency recorded. Assistance is being dispatched.", voice=self.ai_voice, language='en-US')
        response.hangup()
        
        return str(response)
    
    def generate_emergency_confirmation_response(self, triage_result: TriageResult) -> str:
        """Generate confirmation response after triage processing"""
        response = VoiceResponse()
        
        # Standard emergency confirmation message
        confirmation_message = "Emergency recorded. Assistance is being dispatched."
        response.say(confirmation_message, voice=self.ai_voice, language='en-US')
        
        # End call
        response.hangup()
        
        return str(response)
    
    def generate_emergency_safety_response(self, triage_result) -> str:
        """Generate enhanced emergency response with personalized safety instructions"""
        response = VoiceResponse()
        
        # Get AI-generated voice response with safety precautions
        try:
            ai_response = ollama_response_generator.generate_voice_response(triage_result)
            
            logger.info(f"🎤 Generated voice response for {triage_result.emergency_type.value}")
            
            # Say main voice response
            response.say(ai_response['voice_response'], voice=self.ai_voice, language='en-US')
            response.pause(length=1)
            
            # Add safety precautions if available
            if ai_response['safety_precautions']:
                response.say("Here are important safety instructions:", voice=self.ai_voice, language='en-US')
                response.pause(length=1)
                
                for precaution in ai_response['safety_precautions'][:3]:  # Limit to 3 precautions
                    response.say(precaution, voice=self.ai_voice, language='en-US')
                    response.pause(length=1)
            
            # Add caller guidance
            if ai_response['caller_guidance']:
                response.say(ai_response['caller_guidance'], voice=self.ai_voice, language='en-US')
                response.pause(length=1)
            
            # For critical emergencies, keep line open
            if ai_response['is_life_threatening']:
                response.say("Stay on the line. I'm here with you.", voice=self.ai_voice, language='en-US')
                gather = Gather(
                    input='speech',
                    timeout=10,
                    action='/api/voice/process',
                    method='POST',
                    language='en-US',
                    speech_timeout=5,
                    speech_model='phone_call'
                )
                gather.say("If your situation changes, please tell me.", voice=self.ai_voice, language='en-US')
                response.append(gather)
            else:
                response.say("Keep your phone nearby. Help is on the way.", voice=self.ai_voice, language='en-US')
                response.hangup()
            
        except Exception as e:
            logger.error(f"❌ Error generating AI voice response: {e}")
            # Fallback to basic response
            response.say(f"Emergency recorded. {triage_result.assigned_service.value} is being dispatched.", 
                        voice=self.ai_voice, language='en-US')
            response.hangup()
        
        return str(response)
    
    def generate_emergency_safety_response_with_precautions(self, triage_result) -> str:
        """Alias for enhanced response (same as generate_emergency_safety_response)"""
        return self.generate_emergency_safety_response(triage_result)
        
        # Reassurance and final guidance
        reassurance = self._get_reassurance_message(emergency_type, severity_level)
        response.say(reassurance, voice=self.ai_voice, language='en-US')
        
        # Keep line open for critical emergencies
        if severity_level in ['Level 1', 'Level 2']:
            response.say("Stay on the line. I'll stay with you until help arrives.", voice=self.ai_voice, language='en-US')
            # Create a loop to keep caller engaged
            gather = Gather(
                input='speech',
                timeout=10,
                action='/api/voice/process',
                method='POST',
                language='en-US',
                speech_timeout=5,
                speech_model='phone_call'
            )
            gather.say("If your situation changes, please tell me immediately.", voice=self.ai_voice, language='en-US')
            response.append(gather)
        else:
            # For less critical emergencies, provide final guidance
            response.say("Keep your phone nearby. Help is on the way.", voice=self.ai_voice, language='en-US')
            response.hangup()
        
        return str(response)
    
    def _get_safety_instructions(self, emergency_type, severity_level):
        """Get personalized safety instructions based on emergency type and severity"""
        instructions = []
        
        if emergency_type == 'fire':
            instructions = [
                "Get everyone out of the building immediately.",
                "Do not use elevators. Use stairs only.",
                "Feel doors before opening. If hot, find another exit.",
                "Stay low to avoid smoke inhalation.",
                "Once outside, move far away from the building."
            ]
        elif emergency_type == 'medical':
            instructions = [
                "Check if the person is breathing and conscious.",
                "If not breathing, start CPR if you're trained.",
                "Control any bleeding with direct pressure.",
                "Keep the person warm and comfortable.",
                "Clear the area for emergency responders."
            ]
        elif emergency_type == 'accident':
            instructions = [
                "Check for injuries and move to a safe location.",
                "Turn on hazard lights if in a vehicle.",
                "Do not move anyone with serious injuries.",
                "Call for additional help if needed.",
                "Document the scene if safe to do so."
            ]
        elif emergency_type == 'police':
            instructions = [
                "Move to a safe location immediately.",
                "Lock doors and windows if possible.",
                "Do not confront the suspect.",
                "Stay quiet and hide if danger is nearby.",
                "Call 911 if you haven't already."
            ]
        else:
            instructions = [
                "Stay calm and assess your situation.",
                "Move to a safe location if possible.",
                "Follow any emergency procedures you know.",
                "Keep your phone available for updates."
            ]
        
        # Adjust instructions based on severity
        if severity_level == 'Level 1':
            instructions.insert(0, "This is a critical emergency. Act immediately.")
        elif severity_level == 'Level 2':
            instructions.insert(0, "This is urgent. Please act quickly but stay calm.")
        
        return instructions[:5]  # Limit to 5 most important instructions
    
    def _get_reassurance_message(self, emergency_type, severity_level):
        """Get personalized reassurance message"""
        if severity_level == 'Level 1':
            return "Help is arriving as fast as possible. You're not alone."
        elif severity_level == 'Level 2':
            return "Emergency services are prioritizing your call. Stay safe."
        elif severity_level == 'Level 3':
            return "Help is on the way. Please follow the safety instructions."
        else:
            return "Your situation has been recorded. Help will arrive soon."
    
    def generate_welcome_response(self) -> str:
        """Generate initial TwiML response for incoming call"""
        response = VoiceResponse()
        
        # Create gather to capture user speech
        gather = Gather(
            input='speech',
            timeout=settings.SPEECH_TIMEOUT,
            action='/api/voice/process',
            method='POST',
            language='en-US'
        )
        
        welcome_message = f"Hello! This is {settings.AI_ASSISTANT_NAME}, your AI assistant. How can I help you today?"
        gather.say(welcome_message, voice=self.ai_voice, language='en-US')
        
        # If no input received, ask again
        gather.say("I didn't catch that. How can I help you?", voice=self.ai_voice, language='en-US')
        
        response.append(gather)
        
        # If no speech detected after timeout, end call
        response.say("Thank you for calling. Goodbye!", voice=self.ai_voice, language='en-US')
        response.hangup()
        
        return str(response)
    
    def generate_conversation_response(self, ai_response: str) -> str:
        """Generate TwiML response with AI speaking"""
        response = VoiceResponse()
        
        # Create gather for next user input
        gather = Gather(
            input='speech',
            timeout=settings.SPEECH_TIMEOUT,
            action='/api/voice/process',
            method='POST',
            language='en-US'
        )
        
        # Say AI response
        gather.say(ai_response, voice=self.ai_voice, language='en-US')
        
        response.append(gather)
        
        # If no speech detected, say goodbye
        response.say("Thank you for calling. Goodbye!", voice=self.ai_voice, language='en-US')
        response.hangup()
        
        return str(response)
    
    def generate_error_response(self, error_message: str = "I'm sorry, I'm experiencing technical difficulties") -> str:
        """Generate TwiML response for error cases"""
        response = VoiceResponse()
        
        response.say(error_message, voice=self.ai_voice, language='en-US')
        response.say("Please try again later. Goodbye!", voice=self.ai_voice, language='en-US')
        response.hangup()
        
        return str(response)
    
    def generate_goodbye_response(self) -> str:
        """Generate TwiML response for ending call"""
        response = VoiceResponse()
        
        response.say("Thank you for calling. Have a great day! Goodbye!", voice=self.ai_voice, language='en-US')
        response.hangup()
        
        return str(response)


# Global instance
twilio_service = TwilioService()
