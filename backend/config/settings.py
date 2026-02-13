import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    def __init__(self):
        # AI Provider Configuration
        self.AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")
        
        # OpenAI Configuration
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        # Gemini Configuration
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        
        # Twilio Configuration
        self.TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
        self.TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
        self.TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
        
        # Server Configuration
        self.HOST = os.getenv("HOST", "0.0.0.0")
        self.PORT = int(os.getenv("PORT", "8000"))
        
        # AI Assistant Configuration
        self.AI_ASSISTANT_NAME = os.getenv("AI_ASSISTANT_NAME", "Assistant")
        self.AI_ASSISTANT_VOICE = os.getenv("AI_ASSISTANT_VOICE", "alice")
        
        # Conversation Configuration
        self.MAX_CONVERSATION_LENGTH = int(os.getenv("MAX_CONVERSATION_LENGTH", "10"))
        self.SPEECH_TIMEOUT = int(os.getenv("SPEECH_TIMEOUT", "5"))


settings = Settings()
