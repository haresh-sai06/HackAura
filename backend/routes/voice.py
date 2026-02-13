from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import Response
from typing import Optional
import logging
from backend.services import openai_service, twilio_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/voice")
async def handle_incoming_call(request: Request):
    """Handle incoming Twilio call webhook"""
    try:
        # Get call details
        form_data = await request.form()
        call_sid = form_data.get('CallSid', '')
        from_number = form_data.get('From', '')
        
        logger.info(f"Incoming call from {from_number}, Call SID: {call_sid}")
        
        # Generate welcome response
        twiml_response = twilio_service.generate_welcome_response()
        
        return Response(content=twiml_response, media_type="application/xml")
        
    except Exception as e:
        logger.error(f"Error handling incoming call: {e}")
        error_response = twilio_service.generate_error_response()
        return Response(content=error_response, media_type="application/xml")


@router.post("/voice/process")
async def process_speech_input(
    request: Request,
    SpeechResult: Optional[str] = Form(None),
    CallSid: Optional[str] = Form(None),
    UnstableSpeechResult: Optional[str] = Form(None)
):
    """Process user speech input and generate AI response"""
    try:
        # Get call SID
        call_sid = CallSid or ''
        
        # Use the stable speech result if available, otherwise use unstable
        user_input = SpeechResult or UnstableSpeechResult or ""
        
        logger.info(f"Processing speech input for call {call_sid}: {user_input}")
        
        if not user_input:
            # No speech detected, generate goodbye response
            twiml_response = twilio_service.generate_goodbye_response()
            return Response(content=twiml_response, media_type="application/xml")
        
        # Check for goodbye keywords
        goodbye_keywords = ['goodbye', 'bye', 'thank you', 'thanks', 'that\'s all', 'done', 'finish']
        if any(keyword in user_input.lower() for keyword in goodbye_keywords):
            twiml_response = twilio_service.generate_goodbye_response()
            return Response(content=twiml_response, media_type="application/xml")
        
        # Generate AI response
        ai_response = await openai_service.generate_response(call_sid, user_input)
        logger.info(f"AI Response for call {call_sid}: {ai_response}")
        
        # Generate TwiML response with AI speech
        twiml_response = twilio_service.generate_conversation_response(ai_response)
        
        return Response(content=twiml_response, media_type="application/xml")
        
    except Exception as e:
        logger.error(f"Error processing speech input: {e}")
        error_response = twilio_service.generate_error_response()
        return Response(content=error_response, media_type="application/xml")


@router.post("/voice/status")
async def handle_call_status(request: Request):
    """Handle call status updates from Twilio"""
    try:
        form_data = await request.form()
        call_sid = form_data.get('CallSid', '')
        call_status = form_data.get('CallStatus', '')
        
        logger.info(f"Call {call_sid} status: {call_status}")
        
        # Clear conversation history when call ends
        if call_status in ['completed', 'failed', 'busy', 'no-answer']:
            openai_service.clear_conversation(call_sid)
            logger.info(f"Cleared conversation history for call {call_sid}")
        
        return Response(status_code=200)
        
    except Exception as e:
        logger.error(f"Error handling call status: {e}")
        return Response(status_code=500)
