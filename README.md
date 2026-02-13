# Voice AI Phone Assistant

A complete Voice AI Phone Assistant using Twilio and OpenAI that enables natural voice conversations through phone calls.

## Architecture

```
User calls phone number → Twilio receives call → Backend server processes → OpenAI generates response → AI speaks back
```

## Features

- **Natural Voice Conversations**: Real-time speech-to-text and text-to-speech
- **Conversation Memory**: Maintains context throughout the call session
- **Modular Design**: Clean separation of concerns with services
- **Easy LLM Replacement**: Swappable AI provider architecture
- **Production Ready**: Proper error handling and logging
- **Twilio Integration**: Full webhook support with TwiML responses

## Project Structure

```
backend/
├── main.py                 # FastAPI server and application entry point
├── routes/
│   ├── __init__.py
│   └── voice.py           # Voice webhook endpoints
├── services/
│   ├── __init__.py
│   ├── openai_service.py  # OpenAI GPT integration
│   └── twilio_service.py  # TwiML response generation
├── config/
│   ├── __init__.py
│   └── settings.py        # Environment configuration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── __init__.py
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- OpenAI API key
- Twilio account with phone number

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy the environment template and configure your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual credentials:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-actual-openai-api-key
OPENAI_MODEL=gpt-3.5-turbo

# Twilio Configuration
TWILIO_ACCOUNT_SID=ACyour-actual-account-sid
TWILIO_AUTH_TOKEN=your-actual-auth-token
TWILIO_PHONE_NUMBER=+1234567890

# Server Configuration
HOST=0.0.0.0
PORT=8000

# AI Assistant Configuration
AI_ASSISTANT_NAME=Assistant
AI_ASSISTANT_VOICE=alice

# Conversation Configuration
MAX_CONVERSATION_LENGTH=10
SPEECH_TIMEOUT=5
```

### 4. Twilio Dashboard Configuration

1. **Log into Twilio Console**: Go to [console.twilio.com](https://console.twilio.com)

2. **Configure Phone Number**:
   - Navigate to Phone Numbers → Manage → Active Numbers
   - Click on your Twilio phone number
   - Scroll down to "Voice & Fax"
   - Set "A CALL COMES IN" to "Webhook"
   - Enter your webhook URL: `https://your-domain.com/api/voice`
   - Set HTTP method to `POST`

3. **Status Callbacks** (Optional but recommended):
   - Set "Status callback URL" to: `https://your-domain.com/api/voice/status`
   - Set HTTP method to `POST`

### 5. Development with ngrok

For local development, use ngrok to expose your local server:

```bash
# Install ngrok (if not already installed)
# Download from https://ngrok.com/download

# Start your FastAPI server
cd backend
python main.py

# In a new terminal, start ngrok
ngrok http 8000
```

Update your Twilio webhook URL to use the ngrok URL:
```
https://your-ngrok-id.ngrok.io/api/voice
```

### 6. Start the Server

```bash
cd backend
python main.py
```

The server will start on `http://localhost:8000`

## Testing

### 1. Health Check

Test that the server is running:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Voice AI Phone Assistant",
  "version": "1.0.0"
}
```

### 2. Webhook Testing

Test the webhook endpoint directly:

```bash
curl -X POST http://localhost:8000/api/voice \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "CallSid=test123&From=%2B15551234567"
```

### 3. End-to-End Testing

1. Call your Twilio phone number
2. You should hear the AI greeting: "Hello! This is Assistant, your AI assistant. How can I help you today?"
3. Speak naturally - the AI will respond
4. Try saying "goodbye" or "thank you" to end the call

## API Endpoints

### Voice Webhook Endpoints

- `POST /api/voice` - Handles incoming Twilio calls
- `POST /api/voice/process` - Processes speech input and generates AI responses
- `POST /api/voice/status` - Handles call status updates

### Utility Endpoints

- `GET /` - Root endpoint with server info
- `GET /health` - Health check endpoint

## Configuration Options

### AI Assistant Settings

- `AI_ASSISTANT_NAME`: Name of your AI assistant
- `AI_ASSISTANT_VOICE`: Twilio voice option (alice, man, woman, etc.)
- `OPENAI_MODEL`: OpenAI model to use (gpt-3.5-turbo, gpt-4, etc.)

### Conversation Settings

- `MAX_CONVERSATION_LENGTH`: Maximum number of messages to remember
- `SPEECH_TIMEOUT`: Seconds to wait for speech input

### Available Twilio Voices

- `alice` (female, British English)
- `man` (male, US English)
- `woman` (female, US English)
- And more - see [Twilio documentation](https://www.twilio.com/docs/voice/twiml/say/text-to-speech)

## Troubleshooting

### Common Issues

1. **Webhook Not Receiving Calls**
   - Verify ngrok is running and accessible
   - Check Twilio webhook URL is correct
   - Ensure firewall allows inbound connections

2. **OpenAI API Errors**
   - Verify API key is valid and has credits
   - Check model name is correct
   - Monitor rate limits

3. **Speech Recognition Issues**
   - Adjust `SPEECH_TIMEOUT` in configuration
   - Check audio quality and connection
   - Verify Twilio speech language settings

### Logging

The application includes comprehensive logging. Check console output for:
- Incoming call details
- Speech recognition results
- AI responses
- Error messages

## Production Deployment

### Environment Variables

Ensure all environment variables are set in production:
- Use secure secret management
- Never commit `.env` files to version control
- Rotate API keys regularly

### Security Considerations

- Validate incoming Twilio requests using request signatures
- Implement rate limiting
- Use HTTPS in production
- Monitor for abuse

### Scaling

- Use a proper WSGI server like Gunicorn
- Implement load balancing for high traffic
- Consider using Redis for conversation storage in distributed environments

## License

This project is provided as-is for educational and development purposes.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Twilio and OpenAI documentation
3. Check server logs for detailed error information
