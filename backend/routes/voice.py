from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import Response
from typing import Optional
import logging
import asyncio
from services import twilio_service
from services.triage_engine import triage_engine
from services.database_service import database_service
from services.websocket_service import websocket_service
from config import settings
from models.database import CallStatus

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/voice")
async def handle_incoming_call(request: Request):
    """Handle incoming Twilio call webhook - Emergency Triage System"""
    try:
        # Get call details
        form_data = await request.form()
        call_sid = form_data.get('CallSid', '')
        from_number = form_data.get('From', '')
        to_number = form_data.get('To', '')
        call_status = form_data.get('CallStatus', '')
        direction = form_data.get('Direction', '')
        
        # Debug logging for incoming call
        logger.debug(f"📞 INCOMING CALL WEBHOOK")
        logger.debug(f"   Call SID: {call_sid}")
        logger.debug(f"   From: {from_number}")
        logger.debug(f"   To: {to_number}")
        logger.debug(f"   Status: {call_status}")
        logger.debug(f"   Direction: {direction}")
        logger.debug(f"   All Form Data: {dict(form_data)}")
        
        logger.info(f"Incoming emergency call from {from_number}, Call SID: {call_sid}")
        
        # Generate emergency triage response using Twilio speech recognition
        twiml_response = twilio_service.generate_emergency_speech_response()
        
        # Debug response
        logger.debug(f"📤 GENERATED TWIML RESPONSE:")
        logger.debug(f"   Response Length: {len(twiml_response)} characters")
        logger.debug(f"   Response Preview: {twiml_response[:200]}...")
        
        return Response(content=twiml_response, media_type="application/xml")
        
    except Exception as e:
        logger.error(f"❌ ERROR HANDLING INCOMING CALL: {e}")
        logger.error(f"🔍 ERROR DETAILS:")
        logger.error(f"   Exception Type: {type(e).__name__}")
        logger.error(f"   Exception Message: {str(e)}")
        logger.error(f"   Call SID: {form_data.get('CallSid', 'Unknown')}")
        error_response = twilio_service.generate_error_response()
        return Response(content=error_response, media_type="application/xml")


@router.post("/voice/process")
async def process_emergency_input(
    request: Request,
    SpeechResult: Optional[str] = Form(None),
    CallSid: Optional[str] = Form(None),
    UnstableSpeechResult: Optional[str] = Form(None)
):
    """Process emergency input using Twilio's free speech recognition and run triage pipeline"""
    try:
        # Get all form data for debugging
        form_data = await request.form()
        
        # Get call SID
        call_sid = CallSid or ''
        
        # Use stable speech result if available, otherwise use unstable
        transcript = SpeechResult or UnstableSpeechResult or ""
        
        if not transcript or len(transcript.strip()) < 5:
            logger.warning(f"⚠️ INSUFFICIENT INPUT - Attempting to keep caller engaged")
            logger.debug(f"   Transcript Length: {len(transcript)}")
            logger.debug(f"   Transcript Stripped: '{transcript.strip()}'")
            twiml_response = twilio_service.generate_emergency_retry_response()
            logger.debug(f"📤 GENERATED RETRY RESPONSE: {twiml_response[:200]}...")
            return Response(content=twiml_response, media_type="application/xml")
        
        # Run triage pipeline
        triage_result = await triage_engine.process(transcript)
        
        # Store call record in database
        try:
            call_data = {
                'call_sid': call_sid,
                'from_number': form_data.get('From', ''),
                'to_number': form_data.get('To', ''),
                'transcript': transcript,
                'emergency_type': triage_result.emergency_type,
                'severity_level': triage_result.severity_level,
                'severity_score': triage_result.severity_score,
                'location_address': triage_result.location,
                'confidence': triage_result.confidence,
                'risk_indicators': triage_result.risk_indicators,
                'assigned_service': triage_result.assigned_service,
                'priority': triage_result.priority,
                'summary': triage_result.summary,
                'status': CallStatus.PENDING,
                'processing_time_ms': triage_result.processing_time_ms,
                'metadata': {
                    'twilio_form_data': dict(form_data),
                    'speech_result': SpeechResult,
                    'unstable_speech_result': UnstableSpeechResult
                }
            }
            
            call_record = database_service.create_call_record(call_data)
            logger.info(f"📞 Stored call record: {call_record.id}")
            
            # Broadcast new call to WebSocket clients
            if websocket_service.sio:
                await websocket_service.broadcast_new_call(call_record)
            
        except Exception as db_error:
            logger.error(f"❌ Failed to store call record: {db_error}")
            # Continue processing even if database storage fails
        
        # Simplified logging - only key information
        logger.info(f"🎤 Voice Input: '{transcript}'")
        logger.info(f"🏥 Classification: {triage_result.emergency_type.value}")
        logger.info(f"🚨 Severity Level: {triage_result.severity_level.value}")
        
        # Generate response
        twiml_response = twilio_service.generate_emergency_safety_response(triage_result)
        
        return Response(content=twiml_response, media_type="application/xml")
        
    except Exception as e:
        logger.error(f"❌ ERROR PROCESSING EMERGENCY INPUT: {e}")
        logger.error(f"🔍 ERROR DETAILS:")
        logger.error(f"   Call SID: {CallSid}")
        logger.error(f"   SpeechResult: '{SpeechResult}'")
        logger.error(f"   UnstableSpeechResult: '{UnstableSpeechResult}'")
        logger.error(f"   Exception Type: {type(e).__name__}")
        logger.error(f"   Exception Message: {str(e)}")
        import traceback
        logger.error(f"   Traceback: {traceback.format_exc()}")
        error_response = twilio_service.generate_error_response()
        logger.debug(f"📤 ERROR RESPONSE: {error_response}")
        return Response(content=error_response, media_type="application/xml")


@router.post("/voice/status")
async def handle_call_status(request: Request):
    """Handle call status updates from Twilio - Emergency Triage System"""
    try:
        form_data = await request.form()
        call_sid = form_data.get('CallSid', '')
        call_status = form_data.get('CallStatus', '')
        call_duration = form_data.get('CallDuration', '0')
        
        logger.info(f"Emergency call {call_sid} status: {call_status}")
        
        # Log call completion for audit
        if call_status in ['completed', 'failed', 'busy', 'no-answer']:
            logger.info(f"Emergency call {call_sid} ended with status: {call_status}")
        
        return Response(status_code=200)
        
    except Exception as e:
        logger.error(f"Error handling call status: {e}")
        return Response(status_code=500)
