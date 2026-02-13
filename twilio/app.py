"""
RAPID-100 AI-Assisted Emergency Call Triage System
Flask backend with Twilio integration for emergency call processing
"""

import os
import requests
import logging
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Say, Record
import whisper
import re
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Load Whisper model (will download on first run)
print("Loading Whisper model...")
whisper_model = whisper.load_model("base")
print("Whisper model loaded successfully!")

def classify_emergency(transcript):
    """
    Classify emergency type based on transcript content
    Returns: emergency_type, severity_level
    """
    transcript_lower = transcript.lower()
    
    # Define keywords for each emergency type
    emergency_keywords = {
        'Fire': ['fire', 'burning', 'smoke', 'flames', 'explosion', 'burn', 'caught fire'],
        'Medical': ['heart attack', 'stroke', 'bleeding', 'unconscious', 'chest pain', 'difficulty breathing', 
                   'medical emergency', 'ambulance', 'hospital', 'injury', 'wound', 'fainted', 'seizure'],
        'Accident': ['accident', 'crash', 'collision', 'car crash', 'traffic accident', 'fell', 'injured',
                    'hit by car', 'vehicle accident', 'road accident'],
        'Crime': ['robbery', 'theft', 'assault', 'attack', 'gun', 'weapon', 'shooting', 'violence',
                 'break in', 'burglary', 'mugging', 'threat', 'dangerous person']
    }
    
    # Count keyword matches for each category
    scores = {}
    for emergency_type, keywords in emergency_keywords.items():
        score = 0
        for keyword in keywords:
            if keyword in transcript_lower:
                score += 1
        scores[emergency_type] = score
    
    # Determine emergency type (highest score, or Unknown if no matches)
    max_score = max(scores.values())
    if max_score == 0:
        emergency_type = 'Unknown'
    else:
        emergency_type = max(scores, key=scores.get)
    
    # Determine severity level based on keywords and context
    severity_keywords = {
        'Critical': ['critical', 'life threatening', 'unconscious', 'not breathing', 'severe bleeding', 
                    'heart attack', 'stroke', 'gun', 'shooting', 'explosion'],
        'High': ['serious', 'major', 'severe', 'emergency', 'urgent', 'immediate', 'badly injured'],
        'Medium': ['injured', 'pain', 'accident', 'fire', 'medical', 'need help'],
        'Low': ['minor', 'small', 'slight', 'concern', 'worried']
    }
    
    severity_level = 'Medium'  # Default
    for level, keywords in severity_keywords.items():
        if any(keyword in transcript_lower for keyword in keywords):
            severity_level = level
            break
    
    return emergency_type, severity_level

def download_audio_from_twilio(recording_url, account_sid, auth_token):
    """
    Download audio recording from Twilio
    """
    try:
        # Add .mp3 extension to the URL
        audio_url = f"{recording_url}.mp3"
        
        # Download the audio file
        response = requests.get(
            audio_url,
            auth=(account_sid, auth_token),
            timeout=30
        )
        
        if response.status_code == 200:
            # Save as call.wav
            with open('call.wav', 'wb') as f:
                f.write(response.content)
            logger.info("Audio file downloaded and saved as call.wav")
            return True
        else:
            logger.error(f"Failed to download audio: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"Error downloading audio: {str(e)}")
        return False

def transcribe_audio():
    """
    Transcribe audio using Whisper
    """
    try:
        if not os.path.exists('call.wav'):
            logger.error("call.wav file not found")
            return None
        
        logger.info("Starting transcription...")
        result = whisper_model.transcribe('call.wav')
        transcript = result['text']
        logger.info(f"Transcription completed: {transcript}")
        return transcript
        
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        return None

@app.route('/voice', methods=['POST'])
def voice_handler():
    """
    Handle incoming voice calls - answer and record
    """
    response = VoiceResponse()
    
    # Answer the call with a welcome message
    response.say("Welcome to RAPID-100 Emergency Triage System. Please describe your emergency after the beep.")
    
    # Record the caller's speech (30 seconds)
    response.record(
        max_length=30,
        action="/process_recording",  # This URL will be called after recording
        method="POST",
        play_beep=True,
        transcribe=False  # We'll use our own transcription
    )
    
    # If recording fails or times out
    response.say("Thank you for calling. If this is a real emergency, please hang up and dial your local emergency number.")
    response.hangup()
    
    return Response(str(response), mimetype='text/xml')

@app.route('/process_recording', methods=['POST'])
def process_recording():
    """
    Process the recorded audio - download, transcribe, and classify
    """
    try:
        # Get Twilio parameters
        recording_url = request.form.get('RecordingUrl')
        account_sid = request.form.get('AccountSid')
        
        if not recording_url:
            logger.error("No recording URL provided")
            return Response("Error: No recording URL", status=400)
        
        # For authentication, you should use your actual Account SID and Auth Token
        # In production, store these as environment variables
        auth_token = os.getenv('TWILIO_AUTH_TOKEN', 'your_auth_token_here')
        
        logger.info(f"Processing recording from: {recording_url}")
        
        # Step 1: Download audio from Twilio
        if download_audio_from_twilio(recording_url, account_sid, auth_token):
            logger.info("✓ Audio download successful")
        else:
            logger.error("✗ Audio download failed")
            return Response("Error downloading audio", status=500)
        
        # Step 2: Transcribe the audio
        transcript = transcribe_audio()
        if transcript:
            logger.info("✓ Transcription successful")
        else:
            logger.error("✗ Transcription failed")
            return Response("Error transcribing audio", status=500)
        
        # Step 3: Classify the emergency
        emergency_type, severity_level = classify_emergency(transcript)
        
        # Step 4: Print results to terminal
        print("\n" + "="*60)
        print("🚨 RAPID-100 EMERGENCY TRIAGE RESULTS")
        print("="*60)
        print(f"📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📝 Transcript: {transcript}")
        print(f"🚨 Emergency Type: {emergency_type}")
        print(f"⚠️  Severity Level: {severity_level}")
        print("="*60 + "\n")
        
        # Log to system
        logger.info(f"Emergency classified: {emergency_type} - {severity_level}")
        
        # Send response to caller
        response = VoiceResponse()
        response.say("Thank you for your information. Emergency services have been notified. Please stay safe.")
        response.hangup()
        
        return Response(str(response), mimetype='text/xml')
        
    except Exception as e:
        logger.error(f"Error processing recording: {str(e)}")
        return Response(f"Error: {str(e)}", status=500)

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "RAPID-100 Emergency Triage"}

if __name__ == '__main__':
    print("🚀 Starting RAPID-100 Emergency Triage System...")
    print("📞 Server will be available on http://localhost:5000")
    print("🔧 Use ngrok to expose this server to Twilio")
    print("📋 Available endpoints:")
    print("   POST /voice - Handle incoming calls")
    print("   POST /process_recording - Process recorded audio")
    print("   GET /health - Health check")
    print("\n⚠️  Make sure to set your Twilio credentials as environment variables:")
    print("   TWILIO_AUTH_TOKEN=your_auth_token")
    print("\n" + "="*60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
