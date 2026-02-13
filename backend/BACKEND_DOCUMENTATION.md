# HackAura Backend - Structured Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Project Structure](#project-structure)
4. [Core Components](#core-components)
5. [API Documentation](#api-documentation)
6. [Configuration](#configuration)
7. [Dependencies](#dependencies)
8. [Development Guide](#development-guide)
9. [Deployment](#deployment)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

**HackAura Backend** is a Voice AI Phone Assistant system that enables natural voice conversations through phone calls using Twilio integration and AI services (OpenAI/Gemini).

### Key Features
- 🤖 **Multi-AI Support**: OpenAI GPT and Google Gemini integration
- 📞 **Twilio Integration**: Complete voice call handling
- 💬 **Conversation Memory**: Context-aware dialogue management
- 🔧 **Modular Architecture**: Clean separation of concerns
- 🚀 **Production Ready**: Error handling, logging, and monitoring

---

## 🏗️ Architecture

### System Flow
```
User Phone Call → Twilio → Webhook → Backend Server → AI Service → Response → Twilio → User
```

### Technology Stack
- **Backend Framework**: FastAPI (primary) / Flask (alternative)
- **AI Services**: OpenAI GPT, Google Gemini
- **Communication**: Twilio Voice API
- **Configuration**: Environment-based settings
- **Language**: Python 3.8+

---

## 📁 Project Structure

```
backend/
├── 📄 main.py                    # FastAPI server (primary implementation)
├── 📄 main_flask.py             # Flask server (alternative implementation)
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env.example             # Environment variables template
├── 📄 .env                     # Runtime environment (git-ignored)
├── 📁 app/                     # Application modules
│   ├── 📄 __init__.py
│   └── 📁 models/             # Data models (currently empty)
│       └── 📄 __init__.py
├── 📁 config/                 # Configuration management
│   ├── 📄 __init__.py
│   └── 📄 settings.py        # Centralized settings
├── 📁 routes/                 # API route handlers
│   ├── 📄 __init__.py
│   └── 📄 voice.py           # Voice webhook endpoints
├── 📁 services/               # Business logic services
│   ├── 📄 __init__.py
│   ├── 📄 gemini_service.py  # Google Gemini integration
│   └── 📄 twilio_service.py  # Twilio webhook handling
└── 📄 __init__.py            # Package initialization
```

---

## 🔧 Core Components

### 1. Configuration Management (`config/settings.py`)

**Purpose**: Centralized configuration with environment-based settings

#### Configuration Categories
```python
class Settings:
    # AI Provider Configuration
    AI_PROVIDER: str = "gemini"  # or "openai"
    
    # OpenAI Configuration
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Gemini Configuration
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"
    
    # Twilio Configuration
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # AI Assistant Configuration
    AI_ASSISTANT_NAME: str = "Assistant"
    AI_ASSISTANT_VOICE: str = "alice"
    
    # Conversation Configuration
    MAX_CONVERSATION_LENGTH: int = 10
    SPEECH_TIMEOUT: int = 5
```

### 2. AI Services (`services/`)

#### Gemini Service (`services/gemini_service.py`)
**Purpose**: Google Gemini AI integration for conversation handling

**Key Methods**:
- `generate_response(call_sid, user_input)`: Generate AI responses with context
- `get_conversation_history(call_sid)`: Retrieve call-specific history
- `add_to_conversation(call_sid, role, content)`: Add messages to history
- `clear_conversation(call_sid)`: Clean up call history

**Features**:
- ✅ Per-call conversation memory
- ✅ Context-aware responses
- ✅ Automatic history pruning
- ✅ Error handling with fallbacks

#### Twilio Service (`services/twilio_service.py`)
**Purpose**: TwiML response generation and call flow management

**Key Methods**:
- `generate_welcome_response()`: Initial call greeting
- `generate_conversation_response(ai_response)`: AI response with speech gathering
- `generate_error_response(error_message)`: Error handling TwiML
- `generate_goodbye_response()`: Call termination

**Features**:
- ✅ Speech input gathering with timeout
- ✅ Multiple voice options (alice, man, woman)
- ✅ Automatic call flow management
- ✅ Comprehensive error handling

### 3. API Routes (`routes/voice.py`)
**Purpose**: FastAPI route handlers for voice webhooks

#### Endpoints Overview
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/voice` | Handle incoming Twilio calls |
| POST | `/api/voice/process` | Process speech input and generate AI responses |
| POST | `/api/voice/status` | Handle call status updates |

**Features**:
- ✅ Async request handling
- ✅ Form data parsing for Twilio webhooks
- ✅ Goodbye keyword detection
- ✅ Automatic conversation cleanup

### 4. Server Implementations

#### FastAPI Server (`main.py`) - **Primary**
**Purpose**: Production-ready async web server

**Features**:
- 🚀 FastAPI framework with automatic OpenAPI documentation
- 🌐 CORS middleware for cross-origin requests
- 📝 Comprehensive logging
- 💓 Health check endpoints
- 🔗 Router-based architecture

#### Flask Server (`main_flask.py`) - **Alternative**
**Purpose**: Synchronous alternative implementation

**Features**:
- 🌿 Flask framework for simpler deployment
- 🔄 Same API endpoints as FastAPI version
- 🎛️ Dynamic AI provider switching
- ⚡ Identical functionality with different framework

---

## 📡 API Documentation

### Voice Webhook Endpoints

#### 1. Handle Incoming Call
```http
POST /api/voice
Content-Type: application/x-www-form-urlencoded

CallSid=CA123&From=+15551234567&To=+1234567890
```

**Response**: TwiML with welcome message and speech gathering

#### 2. Process Speech Input
```http
POST /api/voice/process
Content-Type: application/x-www-form-urlencoded

CallSid=CA123&SpeechResult=Hello there&UnstableSpeechResult=Hello
```

**Response**: TwiML with AI response and next speech gathering

#### 3. Call Status Update
```http
POST /api/voice/status
Content-Type: application/x-www-form-urlencoded

CallSid=CA123&CallStatus=completed
```

**Response**: HTTP 200 (conversation history cleared)

### Utility Endpoints

#### Health Check
```http
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "service": "Voice AI Phone Assistant",
  "version": "1.0.0"
}
```

#### Server Info
```http
GET /
```

**Response**:
```json
{
  "message": "Voice AI Phone Assistant is running",
  "status": "active",
  "endpoints": {
    "voice_webhook": "/api/voice",
    "process_speech": "/api/voice/process",
    "call_status": "/api/voice/status"
  }
}
```

---

## ⚙️ Configuration

### Environment Variables

#### Required Variables
```bash
# AI Provider Selection
AI_PROVIDER=gemini  # or "openai"

# OpenAI Configuration (if using OpenAI)
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-3.5-turbo

# Gemini Configuration (if using Gemini)
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash

# Twilio Configuration
TWILIO_ACCOUNT_SID=ACyour-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=+1234567890
```

#### Optional Variables
```bash
# Server Configuration
HOST=0.0.0.0
PORT=8000

# AI Assistant Configuration
AI_ASSISTANT_NAME=Assistant
AI_ASSISTANT_VOICE=alice  # alice, man, woman

# Conversation Configuration
MAX_CONVERSATION_LENGTH=10
SPEECH_TIMEOUT=5
```

### Available Twilio Voices
- `alice` (female, British English)
- `man` (male, US English)
- `woman` (female, US English)
- And more - see [Twilio documentation](https://www.twilio.com/docs/voice/twiml/say/text-to-speech)

---

## 📦 Dependencies

### Core Dependencies (`requirements.txt`)
```
fastapi==0.104.1          # Web framework (primary)
uvicorn[standard]==0.24.0 # ASGI server
openai==1.3.7            # OpenAI API client
twilio==8.10.0           # Twilio API client
python-dotenv==1.0.0     # Environment variable management
pydantic==2.5.0          # Data validation
pydantic-settings==2.1.0 # Settings management
```

### Additional Dependencies for Gemini
```bash
pip install google-generativeai
```

---

## 🛠️ Development Guide

### Setup Instructions

#### 1. Clone and Navigate
```bash
cd backend
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
pip install google-generativeai  # For Gemini support
```

#### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

#### 4. Start Development Server

**Using FastAPI (Recommended)**:
```bash
python main.py
```

**Using Flask (Alternative)**:
```bash
python main_flask.py
```

### Testing with ngrok

#### 1. Start ngrok
```bash
ngrok http 8000
```

#### 2. Update Twilio Webhook
In Twilio Console, set webhook URL to:
```
https://your-ngrok-id.ngrok.io/api/voice
```

#### 3. Test Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Webhook test
curl -X POST http://localhost:8000/api/voice \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "CallSid=test123&From=%2B15551234567"
```

### Code Structure Patterns

#### Service Layer Pattern
```python
# services/example_service.py
class ExampleService:
    def __init__(self):
        # Initialize service
        pass
    
    def method_name(self, param: str) -> str:
        # Business logic
        return result

# Global instance
example_service = ExampleService()
```

#### Route Handler Pattern
```python
# routes/example.py
from fastapi import APIRouter, Request
from services import example_service

router = APIRouter()

@router.post("/endpoint")
async def handle_request(request: Request):
    # Parse request
    # Call service
    # Return response
    pass
```

---

## 🚀 Deployment

### Production Considerations

#### Environment Setup
- ✅ Use secure secret management for API keys
- ✅ Never commit `.env` files to version control
- ✅ Rotate API keys regularly
- ✅ Use HTTPS in production

#### Security
- 🔒 Validate incoming Twilio requests using signatures
- 🚦 Implement rate limiting
- 🛡️ Use proper authentication for admin endpoints
- 📊 Monitor for abuse

#### Scaling
- ⚖️ Use Gunicorn or similar WSGI server
- 🔄 Implement load balancing for high traffic
- 💾 Consider Redis for conversation storage
- 📈 Set up monitoring and alerting

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

---

## 🔍 Troubleshooting

### Common Issues

#### 1. Webhook Not Receiving Calls
**Symptoms**: No incoming requests to backend
**Solutions**:
- Verify ngrok is running and accessible
- Check Twilio webhook URL is correct
- Ensure firewall allows inbound connections
- Validate webhook URL format

#### 2. OpenAI API Errors
**Symptoms**: AI responses failing
**Solutions**:
- Verify API key is valid and has credits
- Check model name is correct
- Monitor rate limits
- Check network connectivity

#### 3. Gemini API Errors
**Symptoms**: Gemini responses failing
**Solutions**:
- Verify GEMINI_API_KEY is valid
- Check model name (gemini-2.5-flash)
- Ensure google-generativeai is installed
- Check API quota limits

#### 4. Speech Recognition Issues
**Symptoms**: Poor speech-to-text accuracy
**Solutions**:
- Adjust `SPEECH_TIMEOUT` in configuration
- Check audio quality and connection
- Verify Twilio speech language settings
- Test with different voice options

### Debugging

#### Enable Detailed Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Monitor Call Flow
```bash
# Check server logs for:
- Incoming call details
- Speech recognition results
- AI responses
- Error messages
```

#### Test Components Individually
```python
# Test AI service directly
from services import gemini_service
response = await gemini_service.generate_response("test", "Hello")

# Test TwiML generation
from services import twilio_service
twiml = twilio_service.generate_welcome_response()
```

---

## 📝 Additional Notes

### Goodbye Keywords
The system automatically ends calls when detecting:
- "goodbye", "bye"
- "thank you", "thanks"
- "that's all", "done", "finish"

### Conversation Memory
- Each call has isolated conversation history
- History is automatically pruned to `MAX_CONVERSATION_LENGTH`
- History is cleared when calls end
- Context is maintained throughout the call session

### Error Handling
- All endpoints have comprehensive try-catch blocks
- User-friendly error messages are spoken to users
- Detailed errors are logged for debugging
- Graceful degradation on service failures

---

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review Twilio and AI service documentation
3. Check server logs for detailed error information
4. Verify environment configuration
5. Test with ngrok for local development

---

*Last Updated: February 2026*
*Version: 1.0.0*
