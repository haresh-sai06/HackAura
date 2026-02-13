import os
import tempfile
import logging
import requests
from typing import Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class AudioDownloader:
    def __init__(self):
        self.timeout = 30  # 30 seconds timeout for downloads
        self.chunk_size = 8192  # 8KB chunks
    
    def download_from_twilio(self, recording_url: str) -> Optional[str]:
        """
        Download audio file from Twilio recording URL
        
        Args:
            recording_url: Twilio recording URL
            
        Returns:
            Local file path if successful, None otherwise
        """
        try:
            logger.info(f"Downloading audio from: {recording_url}")
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(
                suffix='.mp3',  # Twilio typically provides MP3
                delete=False
            )
            temp_file.close()
            
            # Download the file
            response = requests.get(
                recording_url,
                stream=True,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            # Save to temporary file
            with open(temp_file.name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    if chunk:
                        f.write(chunk)
            
            file_size = os.path.getsize(temp_file.name)
            logger.info(f"Audio downloaded successfully: {temp_file.name} ({file_size} bytes)")
            
            return temp_file.name
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download audio from Twilio: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during audio download: {e}")
            return None
    
    def download_from_url(self, url: str) -> Optional[str]:
        """
        Generic audio file downloader from URL
        
        Args:
            url: URL of the audio file
            
        Returns:
            Local file path if successful, None otherwise
        """
        try:
            logger.info(f"Downloading audio from URL: {url}")
            
            # Parse URL to determine file extension
            parsed_url = urlparse(url)
            path = parsed_url.path
            file_extension = os.path.splitext(path)[1] or '.mp3'
            
            # Create temporary file with appropriate extension
            temp_file = tempfile.NamedTemporaryFile(
                suffix=file_extension,
                delete=False
            )
            temp_file.close()
            
            # Download the file
            response = requests.get(
                url,
                stream=True,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            # Save to temporary file
            with open(temp_file.name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    if chunk:
                        f.write(chunk)
            
            file_size = os.path.getsize(temp_file.name)
            logger.info(f"Audio downloaded successfully: {temp_file.name} ({file_size} bytes)")
            
            return temp_file.name
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download audio from URL: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during audio download: {e}")
            return None
    
    def cleanup_file(self, file_path: str) -> bool:
        """
        Clean up temporary file
        
        Args:
            file_path: Path to file to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
                return True
            else:
                logger.warning(f"File not found for cleanup: {file_path}")
                return False
        except Exception as e:
            logger.error(f"Failed to cleanup file {file_path}: {e}")
            return False
    
    def validate_audio_file(self, file_path: str) -> bool:
        """
        Validate that downloaded file is a valid audio file
        
        Args:
            file_path: Path to downloaded file
            
        Returns:
            True if valid audio file, False otherwise
        """
        try:
            # Check file size
            if not os.path.exists(file_path):
                logger.error(f"Audio file does not exist: {file_path}")
                return False
            
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                logger.error(f"Audio file is empty: {file_path}")
                return False
            
            # Check file extension
            valid_extensions = ['.mp3', '.wav', '.ogg', '.m4a', '.flac']
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension not in valid_extensions:
                logger.warning(f"Unexpected audio file extension: {file_extension}")
                # Still proceed, but log warning
            
            # TODO: Add more sophisticated audio validation if needed
            # For now, basic checks should suffice
            
            logger.info(f"Audio file validation passed: {file_path} ({file_size} bytes)")
            return True
            
        except Exception as e:
            logger.error(f"Audio file validation failed: {e}")
            return False


# Global instance
audio_downloader = AudioDownloader()
