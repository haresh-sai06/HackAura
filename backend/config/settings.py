import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    def __init__(self):
        # AI Provider Configuration
        self.AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")
        
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
        
        # Emergency System Configuration
        self.SYSTEM_NAME = os.getenv("SYSTEM_NAME", "RAPID-100")
        self.SYSTEM_VERSION = os.getenv("SYSTEM_VERSION", "2.0.0")
        
        # Voice Configuration
        self.AI_ASSISTANT_VOICE = os.getenv("AI_ASSISTANT_VOICE", "alice")
        
        # Emergency Processing Configuration
        self.MAX_RECORDING_LENGTH = int(os.getenv("MAX_RECORDING_LENGTH", "30"))  # seconds
        self.SPEECH_TIMEOUT = int(os.getenv("SPEECH_TIMEOUT", "5"))
        self.MAX_PROCESSING_TIME = int(os.getenv("MAX_PROCESSING_TIME", "5000"))  # milliseconds
        
        # Emergency Classification Thresholds
        self.MIN_CONFIDENCE_THRESHOLD = float(os.getenv("MIN_CONFIDENCE_THRESHOLD", "0.3"))
        self.SEVERITY_THRESHOLD_CRITICAL = float(os.getenv("SEVERITY_THRESHOLD_CRITICAL", "80"))
        self.SEVERITY_THRESHOLD_HIGH = float(os.getenv("SEVERITY_THRESHOLD_HIGH", "60"))
        self.SEVERITY_THRESHOLD_MODERATE = float(os.getenv("SEVERITY_THRESHOLD_MODERATE", "40"))
        
        # Debug Configuration
        self.DEBUG_MODE = os.getenv("DEBUG_MODE", "true").lower() == "true"
        self.VERBOSE_LOGGING = os.getenv("VERBOSE_LOGGING", "true").lower() == "true"
        self.LOG_REQUESTS = os.getenv("LOG_REQUESTS", "true").lower() == "true"
        self.LOG_RESPONSES = os.getenv("LOG_RESPONSES", "true").lower() == "true"
        self.LOG_TRIAGE_STEPS = os.getenv("LOG_TRIAGE_STEPS", "true").lower() == "true"
        
        # Print debug settings on startup
        if self.DEBUG_MODE:
            print("🐛 DEBUG MODE ENABLED")
            print(f"📊 Verbose Logging: {self.VERBOSE_LOGGING}")
            print(f"📝 Log Requests: {self.LOG_REQUESTS}")
            print(f"📤 Log Responses: {self.LOG_RESPONSES}")
            print(f"🎯 Log Triage Steps: {self.LOG_TRIAGE_STEPS}")
            print("=" * 50)


settings = Settings()
