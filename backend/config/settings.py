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
<<<<<<< HEAD
        self.MAX_PROCESSING_TIME = int(os.getenv("MAX_PROCESSING_TIME", "5000"))  # milliseconds
        
        # Emergency Classification Thresholds
        self.MIN_CONFIDENCE_THRESHOLD = float(os.getenv("MIN_CONFIDENCE_THRESHOLD", "0.3"))
        self.SEVERITY_THRESHOLD_CRITICAL = float(os.getenv("SEVERITY_THRESHOLD_CRITICAL", "80"))
        self.SEVERITY_THRESHOLD_HIGH = float(os.getenv("SEVERITY_THRESHOLD_HIGH", "60"))
        self.SEVERITY_THRESHOLD_MODERATE = float(os.getenv("SEVERITY_THRESHOLD_MODERATE", "40"))
=======
        
        # Email Configuration
        self.SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
        self.SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
        self.SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
        self.FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@hackaura.com")
        
        # Webhook Configuration
        self.WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
        
        # Emergency Configuration
        self.EMERGENCY_AUTO_ESCALATION = os.getenv("EMERGENCY_AUTO_ESCALATION", "true").lower() == "true"
        self.EMERGENCY_RESPONSE_TIME_THRESHOLD = int(os.getenv("EMERGENCY_RESPONSE_TIME_THRESHOLD", "30"))
        self.EMERGENCY_MAX_ESCALATION_LEVEL = int(os.getenv("EMERGENCY_MAX_ESCALATION_LEVEL", "3"))
        
        # Analytics Configuration
        self.ANALYTICS_RETENTION_DAYS = int(os.getenv("ANALYTICS_RETENTION_DAYS", "90"))
        self.ANALYTICS_REAL_TIME_UPDATES = os.getenv("ANALYTICS_REAL_TIME_UPDATES", "true").lower() == "true"
        
        # Team Configuration
        self.TEAM_MAX_CONCURRENT_CALLS = int(os.getenv("TEAM_MAX_CONCURRENT_CALLS", "3"))
        self.TEAM_AUTO_ASSIGN_CALLS = os.getenv("TEAM_AUTO_ASSIGN_CALLS", "true").lower() == "true"
        self.TEAM_SKILL_MATCHING = os.getenv("TEAM_SKILL_MATCHING", "true").lower() == "true"
>>>>>>> 91c63386882b7ea903abf849c9707bba1e9f19a8


settings = Settings()
