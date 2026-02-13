from flask import Flask, request, Response
import logging
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings
from services import twilio_service, gemini_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)


@app.route('/')
def root():
    """Root endpoint to check if server is running"""
    return {
        "message": "Voice AI Phone Assistant is running",
        "status": "active",
        "endpoints": {
            "voice_webhook": "/api/voice",
            "process_speech": "/api/voice/process",
            "call_status": "/api/voice/status"
        }
    }


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Voice AI Phone Assistant",
        "version": "1.0.0"
    }


@app.route('/api/voice', methods=['POST'])
def handle_incoming_call():
    """Handle incoming Twilio call webhook"""
    try:
        # Get call details
        call_sid = request.form.get('CallSid', '')
        from_number = request.form.get('From', '')
        
        logger.info(f"Incoming call from {from_number}, Call SID: {call_sid}")
        
        # Generate welcome response
        twiml_response = twilio_service.generate_welcome_response()
        
        return Response(twiml_response, mimetype='application/xml')
        
    except Exception as e:
        logger.error(f"Error handling incoming call: {e}")
        error_response = twilio_service.generate_error_response()
        return Response(error_response, mimetype='application/xml')


@app.route('/api/voice/process', methods=['POST'])
def process_speech_input():
    """Process user speech input and generate AI response"""
    try:
        # Get call SID
        call_sid = request.form.get('CallSid', '')
        
        # Get speech result
        speech_result = request.form.get('SpeechResult', '')
        unstable_speech_result = request.form.get('UnstableSpeechResult', '')
        
        # Use stable speech result if available, otherwise use unstable
        user_input = speech_result or unstable_speech_result or ""
        
        # DEBUG: Log what Twilio sent us
        logger.info(f" TWILIO SPEECH INPUT for call {call_sid}:")
        logger.info(f"   SpeechResult: '{speech_result}'")
        logger.info(f"   UnstableSpeechResult: '{unstable_speech_result}'")
        logger.info(f"   Final user_input: '{user_input}'")
        
        if not user_input:
            logger.info(f" No speech detected, generating goodbye response")
            # No speech detected, generate goodbye response
            twiml_response = twilio_service.generate_goodbye_response()
            return Response(twiml_response, mimetype='application/xml')
        
        # Check for goodbye keywords
        goodbye_keywords = ['goodbye', 'bye', 'thank you', 'thanks', 'that\'s all', 'done', 'finish']
        if any(keyword in user_input.lower() for keyword in goodbye_keywords):
            twiml_response = twilio_service.generate_goodbye_response()
            return Response(twiml_response, mimetype='application/xml')
        
        # Generate AI response based on provider
        if settings.AI_PROVIDER.lower() == "gemini":
            logger.info(f"🤖 Using Gemini for call {call_sid}")
            logger.info(f"📝 Sending to Gemini: '{user_input}'")
            try:
                import asyncio
                ai_response = asyncio.run(gemini_service.generate_response(call_sid, user_input))
                logger.info(f"✅ Gemini response: {ai_response}")
            except Exception as e:
                logger.error(f"❌ Gemini error: {type(e).__name__}: {str(e)}")
                logger.error(f"🔍 Full error details: {repr(e)}")
                ai_response = "I'm sorry, I'm having trouble understanding. Could you please repeat that?"
        else:
            logger.info(f"🤖 Using OpenAI for call {call_sid}")
            import asyncio
            ai_response = asyncio.run(openai_service.generate_response(call_sid, user_input))
        
        logger.info(f"AI Response for call {call_sid}: {ai_response}")
        
        # Generate TwiML response with AI speech
        twiml_response = twilio_service.generate_conversation_response(ai_response)
        
        return Response(twiml_response, mimetype='application/xml')
        
    except Exception as e:
        logger.error(f"Error processing speech input: {e}")
        error_response = twilio_service.generate_error_response()
        return Response(error_response, mimetype='application/xml')


@app.route('/api/voice/status', methods=['POST'])
def handle_call_status():
    """Handle call status updates from Twilio"""
    try:
        call_sid = request.form.get('CallSid', '')
        call_status = request.form.get('CallStatus', '')
        
        logger.info(f"Call {call_sid} status: {call_status}")
        
        # Clear conversation history when call ends
        if call_status in ['completed', 'failed', 'busy', 'no-answer']:
            if settings.AI_PROVIDER.lower() == "gemini":
                gemini_service.clear_conversation(call_sid)
            else:
                openai_service.clear_conversation(call_sid)
            logger.info(f"Cleared conversation history for call {call_sid}")
        
        return Response(status=200)
        
    except Exception as e:
        logger.error(f"Error handling call status: {e}")
        return Response(status=500)


if __name__ == "__main__":
    logger.info("Starting Voice AI Phone Assistant server...")
    logger.info(f"Server will run on http://{settings.HOST}:{settings.PORT}")
    
    app.run(
        host=settings.HOST,
        port=settings.PORT,
        debug=True
    )
