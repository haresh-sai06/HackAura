# RAPID-100 AI-Assisted Emergency Call Triage System

A Flask-based emergency call triage system that integrates with Twilio for voice calls, uses OpenAI Whisper for speech transcription, and AI-powered emergency classification.

## Features

- 📞 **Twilio Integration**: Answer incoming calls automatically
- 🎙️ **Voice Recording**: 30-second recording of emergency descriptions
- 🔊 **Speech-to-Text**: Local Whisper model for transcription
- 🚨 **Emergency Classification**: Detects Fire, Medical, Accident, Crime, or Unknown
- ⚠️ **Severity Assessment**: Critical, High, Medium, Low priority levels
- 📊 **Terminal Output**: Real-time results display

## Installation

### Prerequisites
- Python 3.8+
- Twilio account (for phone number and credentials)

### Setup Instructions

1. **Clone/Download the project** to your local machine

2. **Navigate to the project directory**:
   ```bash
   cd rapid100-call-ai
   ```

3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   ```bash
   # On Windows:
   set TWILIO_AUTH_TOKEN=your_actual_auth_token
   
   # On Mac/Linux:
   export TWILIO_AUTH_TOKEN=your_actual_auth_token
   ```

## Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Expose with ngrok** (for Twilio webhook):
   ```bash
   ngrok http 5000
   ```

3. **Configure Twilio**:
   - Go to your Twilio console
   - Configure your phone number's voice webhook
   - Set webhook URL to: `https://your-ngrok-url.ngrok.io/voice`
   - Set method to: `HTTP POST`

## API Endpoints

- `POST /voice` - Handles incoming calls and recording
- `POST /process_recording` - Processes recorded audio
- `GET /health` - Health check endpoint

## Example Terminal Output

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

## Emergency Classification Logic

### Emergency Types
- **Fire**: fire, burning, smoke, flames, explosion, burn
- **Medical**: heart attack, stroke, bleeding, unconscious, chest pain
- **Accident**: accident, crash, collision, car crash, fell
- **Crime**: robbery, theft, assault, attack, gun, weapon
- **Unknown**: No clear emergency indicators

### Severity Levels
- **Critical**: life threatening, unconscious, severe bleeding
- **High**: serious, major, severe, urgent
- **Medium**: injured, pain, accident, fire, medical
- **Low**: minor, small, slight, concern

## File Structure

```
rapid100-call-ai/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── call.wav           # Audio file (created during runtime)
```

## Twilio Configuration

1. **Get Twilio Credentials**:
   - Account SID (from Twilio console)
   - Auth Token (from Twilio console)
   - Phone number (with voice capabilities)

2. **Webhook Setup**:
   - Voice URL: `https://your-ngrok-url.ngrok.io/voice`
   - Method: `POST`
   - Accept: `application/xml`

## Testing

You can test the system by:
1. Starting the server and ngrok
2. Calling your Twilio phone number
3. Speaking an emergency description
4. Checking the terminal for classification results

## Security Notes

- Store Twilio credentials as environment variables
- Use HTTPS in production
- Validate and sanitize all inputs
- Implement proper error handling

## Troubleshooting

### Common Issues

1. **Whisper Model Download**: First run downloads ~150MB model
2. **ngrok Connection**: Ensure ngrok is running and accessible
3. **Twilio Webhook**: Verify webhook URL is correct and accessible
4. **Audio File**: Check `call.wav` is created in project directory

### Debug Mode

The app runs in debug mode by default. Check console logs for detailed error information.

## License

This project is for educational and demonstration purposes.
