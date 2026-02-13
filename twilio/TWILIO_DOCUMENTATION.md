# RAPID-100 Twilio Emergency Triage System - Comprehensive Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Project Structure](#project-structure)
4. [Core Components](#core-components)
5. [API Documentation](#api-documentation)
6. [Emergency Classification System](#emergency-classification-system)
7. [Configuration](#configuration)
8. [Dependencies](#dependencies)
9. [Setup & Installation](#setup--installation)
10. [Development Guide](#development-guide)
11. [Testing](#testing)
12. [Deployment](#deployment)
13. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

**RAPID-100** is an AI-assisted emergency call triage system that automatically answers incoming calls, records emergency descriptions, transcribes speech using OpenAI Whisper, and classifies emergencies with severity levels.

### Key Features
- 📞 **Twilio Integration**: Automatic call answering and recording
- 🎙️ **Voice Recording**: 30-second emergency description capture
- 🔊 **Speech-to-Text**: Local Whisper model for accurate transcription
- 🚨 **Emergency Classification**: AI-powered emergency type detection
- ⚠️ **Severity Assessment**: Critical, High, Medium, Low priority levels
- 📊 **Real-time Results**: Terminal output with classification results

---

## 🏗️ System Architecture

### Call Flow Architecture
```
Incoming Call → Twilio → Flask App → Voice Recording → Audio Download → Whisper Transcription → AI Classification → Results Display
```

### Technology Stack
- **Backend Framework**: Flask 2.3.3
- **Communication**: Twilio Voice API
- **Speech Processing**: OpenAI Whisper
- **Machine Learning**: PyTorch for Whisper model
- **HTTP Client**: Requests for audio download
- **Classification**: Rule-based keyword matching

---

## 📁 Project Structure

```
twilio/
├── 📄 app.py              # Main Flask application (233 lines)
├── 📄 requirements.txt    # Python dependencies
├── 📄 README.md          # Basic project documentation
├── 📄 TWILIO_DOCUMENTATION.md  # This comprehensive documentation
└── 📄 call.wav           # Audio file (created during runtime)
```

### File Breakdown
- **`app.py`**: Core Flask application with all endpoints and business logic
- **`requirements.txt`**: Python package dependencies
- **`call.wav`**: Temporary audio storage for downloaded recordings
- **`README.md`**: Basic setup and usage instructions

---

## 🔧 Core Components

### 1. Flask Application (`app.py`)

#### Main Components
```python
# Core imports
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Say, Record
import whisper  # OpenAI Whisper for transcription
import requests  # HTTP client for audio download
```

#### Key Functions

##### `classify_emergency(transcript)`
**Purpose**: Classify emergency type and severity based on transcript

**Emergency Types**:
- **Fire**: fire, burning, smoke, flames, explosion, burn
- **Medical**: heart attack, stroke, bleeding, unconscious, chest pain
- **Accident**: accident, crash, collision, car crash, fell, injured
- **Crime**: robbery, theft, assault, attack, gun, weapon
- **Unknown**: No clear emergency indicators

**Severity Levels**:
- **Critical**: life threatening, unconscious, severe bleeding
- **High**: serious, major, severe, urgent
- **Medium**: injured, pain, accident, fire, medical
- **Low**: minor, small, slight, concern

##### `download_audio_from_twilio(recording_url, account_sid, auth_token)`
**Purpose**: Download recorded audio from Twilio servers

**Process**:
1. Add `.mp3` extension to recording URL
2. Authenticate with Twilio credentials
3. Download audio file
4. Save as `call.wav` in project directory

##### `transcribe_audio()`
**Purpose**: Transcribe audio using Whisper model

**Features**:
- Uses Whisper base model (150MB download on first run)
- Processes `call.wav` file
- Returns text transcript
- Handles file not found and transcription errors

### 2. Twilio Integration

#### TwiML Response Generation
```python
response = VoiceResponse()
response.say("Welcome message...")
response.record(max_length=30, action="/process_recording")
response.say("Thank you message...")
response.hangup()
```

#### Recording Configuration
- **Max Length**: 30 seconds
- **Action URL**: `/process_recording`
- **Method**: POST
- **Play Beep**: True
- **Transcription**: Disabled (using custom Whisper)

---

## 📡 API Documentation

### Endpoints Overview

#### 1. Handle Incoming Call
```http
POST /voice
Content-Type: application/x-www-form-urlencoded
```

**Purpose**: Answer incoming calls and initiate recording

**Response**: TwiML with welcome message and recording instructions

**Flow**:
1. Answer call with welcome message
2. Record caller's speech (30 seconds)
3. Redirect to `/process_recording` after recording
4. Fallback message if recording fails

#### 2. Process Recording
```http
POST /process_recording
Content-Type: application/x-www-form-urlencoded

RecordingUrl=https://api.twilio.com/.../Recordings/RE...
AccountSid=ACyour-account-sid
```

**Purpose**: Download, transcribe, and classify emergency recording

**Process Flow**:
1. Extract recording URL and account SID
2. Download audio from Twilio
3. Transcribe using Whisper
4. Classify emergency type and severity
5. Display results in terminal
6. Send confirmation to caller

**Response**: TwiML with thank you message and call termination

#### 3. Health Check
```http
GET /health
```

**Purpose**: System health monitoring

**Response**:
```json
{
  "status": "healthy",
  "service": "RAPID-100 Emergency Triage"
}
```

---

## 🚨 Emergency Classification System

### Classification Algorithm

#### Step 1: Emergency Type Detection
```python
emergency_keywords = {
    'Fire': ['fire', 'burning', 'smoke', 'flames', 'explosion', 'burn'],
    'Medical': ['heart attack', 'stroke', 'bleeding', 'unconscious', 'chest pain'],
    'Accident': ['accident', 'crash', 'collision', 'car crash', 'fell', 'injured'],
    'Crime': ['robbery', 'theft', 'assault', 'attack', 'gun', 'weapon']
}
```

**Scoring System**:
- Count keyword matches for each category
- Select category with highest score
- Default to "Unknown" if no matches

#### Step 2: Severity Assessment
```python
severity_keywords = {
    'Critical': ['critical', 'life threatening', 'unconscious', 'not breathing'],
    'High': ['serious', 'major', 'severe', 'emergency', 'urgent'],
    'Medium': ['injured', 'pain', 'accident', 'fire', 'medical'],
    'Low': ['minor', 'small', 'slight', 'concern', 'worried']
}
```

**Priority Order**: Critical > High > Medium > Low (first match wins)

### Example Classifications

| Transcript | Emergency Type | Severity |
|------------|----------------|----------|
| "There's a fire in my kitchen" | Fire | Medium |
| "Someone had a heart attack" | Medical | Critical |
| "Car crash on highway" | Accident | High |
| "Robbery with weapon" | Crime | Critical |
| "I need help" | Unknown | Medium |

---

## ⚙️ Configuration

### Environment Variables

#### Required Variables
```bash
# Twilio Authentication
TWILIO_AUTH_TOKEN=your_actual_auth_token
```

#### Optional Variables
```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### Twilio Configuration

#### Required Twilio Setup
1. **Account SID**: From Twilio console
2. **Auth Token**: From Twilio console
3. **Phone Number**: With voice capabilities
4. **Webhook URL**: `https://your-ngrok-url.ngrok.io/voice`
5. **HTTP Method**: POST

#### Webhook Configuration
```
Voice URL: https://your-ngrok-url.ngrok.io/voice
Method: POST
Accept: application/xml
Status Callback: (Optional)
```

---

## 📦 Dependencies

### Core Dependencies (`requirements.txt`)
```
flask==2.3.3              # Web framework
twilio==8.8.0             # Twilio API client
requests==2.31.0          # HTTP client for audio download
openai-whisper==20231117  # Speech-to-text model
torch==2.1.0              # PyTorch for Whisper
torchaudio==2.1.0         # Audio processing for PyTorch
```

### Dependency Breakdown

#### Flask Framework
- **Purpose**: Web server and API endpoints
- **Version**: 2.3.3 (stable)
- **Features**: Request handling, response generation

#### Twilio SDK
- **Purpose**: TwiML generation and API integration
- **Version**: 8.8.0
- **Features**: VoiceResponse, Record, Say components

#### OpenAI Whisper
- **Purpose**: Local speech-to-text transcription
- **Version**: 20231117
- **Model**: Base (150MB, good balance of speed/accuracy)
- **Requirements**: PyTorch for model execution

#### PyTorch
- **Purpose**: Machine learning framework for Whisper
- **Version**: 2.1.0
- **Components**: Core ML operations + audio processing

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- Twilio account with phone number
- ~2GB disk space (for Whisper model)
- Internet connection (for model download)

### Installation Steps

#### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

#### 2. Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

#### 3. Configure Environment
```bash
# Set Twilio auth token (Windows)
set TWILIO_AUTH_TOKEN=your_actual_auth_token

# Set Twilio auth token (Mac/Linux)
export TWILIO_AUTH_TOKEN=your_actual_auth_token
```

#### 4. Verify Setup
```bash
# Test Flask app startup
python app.py
```

### First Run Setup
- Whisper model downloads automatically (~150MB)
- Model stored in cache directory
- Subsequent runs use cached model

---

## 🧪 Development Guide

### Local Development

#### Start Development Server
```bash
python app.py
```

**Output**:
```
🚀 Starting RAPID-100 Emergency Triage System...
📞 Server will be available on http://localhost:5000
🔧 Use ngrok to expose this server to Twilio
Loading Whisper model...
Whisper model loaded successfully!
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[local-ip]:5000
```

#### Setup ngrok for Testing
```bash
# Start ngrok
ngrok http 5000

# Update Twilio webhook URL to:
# https://your-ngrok-id.ngrok.io/voice
```

### Code Structure Patterns

#### Endpoint Handler Pattern
```python
@app.route('/endpoint', methods=['POST'])
def handler():
    try:
        # Extract request data
        param = request.form.get('Parameter')
        
        # Process data
        result = process_function(param)
        
        # Generate response
        response = VoiceResponse()
        response.say("Response message")
        
        return Response(str(response), mimetype='text/xml')
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return Response(f"Error: {str(e)}", status=500)
```

#### Classification Logic Pattern
```python
def classify_emergency(transcript):
    transcript_lower = transcript.lower()
    scores = {}
    
    # Score each category
    for category, keywords in emergency_keywords.items():
        score = sum(1 for keyword in keywords if keyword in transcript_lower)
        scores[category] = score
    
    # Determine best match
    max_score = max(scores.values())
    return max(scores, key=scores.get) if max_score > 0 else 'Unknown'
```

---

## 🧪 Testing

### Manual Testing Process

#### 1. System Setup Test
```bash
# Start server
python app.py

# Check health endpoint
curl http://localhost:5000/health
```

#### 2. Twilio Integration Test
```bash
# Start ngrok
ngrok http 5000

# Configure Twilio webhook
# URL: https://ngrok-id.ngrok.io/voice
# Method: POST
```

#### 3. End-to-End Test
1. Call your Twilio phone number
2. Listen for welcome message
3. Speak emergency description (30 seconds max)
4. Check terminal for classification results
5. Verify confirmation message

### Expected Terminal Output
```
============================================================
🚨 RAPID-100 EMERGENCY TRIAGE RESULTS
============================================================
📅 Timestamp: 2024-01-15 14:30:22
📝 Transcript: There's a fire in my kitchen and it's spreading quickly
🚨 Emergency Type: Fire
⚠️  Severity Level: Critical
============================================================
```

### Test Scenarios

#### Fire Emergency
**Input**: "There's a fire in my kitchen"
**Expected**: Fire - Medium/High (depending on context)

#### Medical Emergency
**Input**: "Someone is having a heart attack"
**Expected**: Medical - Critical

#### Accident
**Input**: "Car crash on the highway"
**Expected**: Accident - High

#### Crime
**Input**: "Robbery with a weapon"
**Expected**: Crime - Critical

#### Unknown
**Input**: "I need some help"
**Expected**: Unknown - Medium

---

## 🚀 Deployment

### Production Considerations

#### Security
- 🔒 Store Twilio credentials as environment variables
- 🛡️ Use HTTPS in production
- ✅ Validate Twilio request signatures
- 🚫 Never hardcode credentials in code

#### Performance
- ⚡ Consider using larger Whisper models for better accuracy
- 💾 Implement audio file cleanup
- 🔄 Add request rate limiting
- 📊 Set up monitoring and logging

#### Scalability
- 📈 Use production WSGI server (Gunicorn)
- 🔄 Load balancing for multiple instances
- 💾 Consider Redis for session storage
- ☁️ Cloud deployment options (AWS, GCP, Azure)

### Docker Deployment

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables
ENV TWILIO_AUTH_TOKEN=${TWILIO_AUTH_TOKEN}

# Start application
CMD ["python", "app.py"]
```

#### Docker Compose
```yaml
version: '3.8'
services:
  rapid100:
    build: .
    ports:
      - "5000:5000"
    environment:
      - TWILIO_AUTH_TOKEN=${TWILIO_AUTH_TOKEN}
    volumes:
      - ./logs:/app/logs
```

### Production Server Setup

#### Gunicorn Configuration
```bash
# Install Gunicorn
pip install gunicorn

# Start with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Systemd Service
```ini
[Unit]
Description=RAPID-100 Emergency Triage
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/rapid100
Environment=TWILIO_AUTH_TOKEN=your_token
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 🔍 Troubleshooting

### Common Issues

#### 1. Whisper Model Download Issues
**Symptoms**: Long startup time, download errors
**Solutions**:
- Check internet connection
- Ensure sufficient disk space (~2GB)
- Verify PyTorch installation
- Check firewall/proxy settings

#### 2. Twilio Webhook Issues
**Symptoms**: No incoming requests, connection errors
**Solutions**:
- Verify ngrok is running and accessible
- Check webhook URL in Twilio console
- Ensure HTTP method is set to POST
- Validate ngrok tunnel stability

#### 3. Audio Download Failures
**Symptoms**: "Error downloading audio" in logs
**Solutions**:
- Verify Twilio credentials (Account SID, Auth Token)
- Check recording URL format
- Ensure network connectivity to Twilio
- Validate authentication

#### 4. Transcription Errors
**Symptoms**: "Transcription failed" or empty results
**Solutions**:
- Check audio file exists (`call.wav`)
- Verify audio file format and integrity
- Ensure Whisper model loaded correctly
- Check audio quality and duration

#### 5. Classification Issues
**Symptoms**: Incorrect emergency type or severity
**Solutions**:
- Review keyword lists in `classify_emergency()`
- Check transcript accuracy
- Verify case-insensitive matching
- Consider adding more keywords

### Debug Mode

#### Enable Detailed Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Monitor Key Metrics
```bash
# Check Flask logs
tail -f /var/log/rapid100/app.log

# Monitor system resources
htop
df -h  # Disk space for model
```

#### Test Components Individually
```python
# Test Whisper directly
import whisper
model = whisper.load_model("base")
result = model.transcribe("test_audio.wav")

# Test classification
emergency_type, severity = classify_emergency("fire emergency")
print(f"Type: {emergency_type}, Severity: {severity}")
```

### Performance Optimization

#### Whisper Model Options
- **Base**: 74MB, Fast, Good accuracy (default)
- **Small**: 244MB, Slower, Better accuracy
- **Medium**: 769MB, Much slower, Best accuracy
- **Large**: 1550MB, Very slow, Excellent accuracy

#### Optimization Tips
- Use appropriate model size for your use case
- Implement audio file cleanup
- Cache classification results
- Monitor memory usage

---

## 📊 Monitoring & Analytics

### Key Metrics to Monitor
- **Call Volume**: Number of incoming calls
- **Transcription Accuracy**: Manual sample checking
- **Classification Accuracy**: Emergency type verification
- **Response Time**: Call processing duration
- **Error Rates**: Failed transcriptions/classifications

### Logging Strategy
```python
# Structured logging
logger.info(f"Call received: {call_sid}")
logger.info(f"Transcription: {transcript}")
logger.info(f"Classification: {emergency_type} - {severity}")
logger.error(f"Error: {error_message}")
```

### Health Checks
- **Application Health**: `/health` endpoint
- **Model Status**: Whisper model loaded
- **Twilio Connectivity**: Webhook accessibility
- **Disk Space**: For audio files and models

---

## 🔄 Future Enhancements

### Potential Improvements
- **Multi-language Support**: Whisper multilingual models
- **Real-time Transcription**: Streaming audio processing
- **Machine Learning Classification**: Replace keyword-based with ML model
- **Database Integration**: Store call history and analytics
- **SMS Notifications**: Send alerts to emergency services
- **Geolocation**: Extract location from caller information

### Advanced Features
- **Voice Biometrics**: Caller identification
- **Sentiment Analysis**: Emotional state detection
- **Priority Queuing**: Based on severity classification
- **Integration APIs**: Connect to emergency services
- **Dashboard**: Web interface for monitoring

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks
- **Log Rotation**: Prevent log files from growing too large
- **Model Updates**: Keep Whisper model current
- **Security Updates**: Regular dependency updates
- **Performance Monitoring**: Track response times and accuracy

### Contact Information
For technical support:
1. Check this documentation first
2. Review application logs
3. Verify Twilio configuration
4. Test with known scenarios

---

*Last Updated: February 2026*
*Version: 1.0.0*
*System: RAPID-100 Emergency Triage*
