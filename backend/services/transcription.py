import openai
import logging
from typing import Optional
from config import settings

logger = logging.getLogger(__name__)


class TranscriptionService:
    def __init__(self):
        # Initialize OpenAI client properly
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        else:
            logger.warning("OpenAI API key not configured")
        
    async def transcribe_audio(self, audio_file_path: str) -> Optional[str]:
        """
        Transcribe audio file using OpenAI Whisper API
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Transcribed text or None if failed
        """
        try:
            logger.info(f"Starting transcription for {audio_file_path}")
            
            with open(audio_file_path, "rb") as audio_file:
                # Use the correct OpenAI API call
                response = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language="en",
                    response_format="text"
                )
            
            transcript = response.strip()
            logger.info(f"Transcription completed: {len(transcript)} characters")
            return transcript
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return None
    
    async def transcribe_audio_url(self, audio_url: str) -> Optional[str]:
        """
        Transcribe audio from URL (for future implementation)
        
        Args:
            audio_url: URL of the audio file
            
        Returns:
            Transcribed text or None if failed
        """
        try:
            # This would require downloading the audio first
            # For now, return None as placeholder
            logger.warning("URL transcription not implemented yet")
            return None
        except Exception as e:
            logger.error(f"URL transcription failed: {e}")
            return None


# Global instance
transcription_service = TranscriptionService()
