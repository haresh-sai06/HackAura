from twilio.twiml.voice_response import VoiceResponse, Gather
from typing import Optional
from config import settings


class TwilioService:
    def __init__(self):
        self.ai_voice = settings.AI_ASSISTANT_VOICE
    
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
    
    def generate_error_response(self, error_message: str = "I'm sorry, I'm experiencing technical difficulties.") -> str:
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
