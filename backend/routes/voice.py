from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import Response
from typing import Optional
import logging
import asyncio
from services import twilio_service
from services.triage_engine import triage_engine
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/voice")
async def handle_incoming_call(request: Request):
    """Handle incoming Twilio call webhook - Emergency Triage System"""
    try:
        # Get call details
        form_data = await request.form()
        call_sid = form_data.get('CallSid', '')
        from_number = form_data.get('From', '')
        
        logger.info(f"Incoming emergency call from {from_number}, Call SID: {call_sid}")
        
        # Generate emergency triage response using Twilio speech recognition
        twiml_response = twilio_service.generate_emergency_speech_response()
        
        return Response(content=twiml_response, media_type="application/xml")
        
    except Exception as e:
        logger.error(f"Error handling incoming emergency call: {e}")
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
        # Get call SID
        call_sid = CallSid or ''
        
        # Use the stable speech result if available, otherwise use unstable
        transcript = SpeechResult or UnstableSpeechResult or ""
        
        # DEBUG: Enhanced logging
        logger.info(f"🚨 EMERGENCY CALL PROCESSING - Call SID: {call_sid}")
        logger.info(f"📝 RAW SPEECH INPUT:")
        logger.info(f"   SpeechResult: '{SpeechResult}'")
        logger.info(f"   UnstableSpeechResult: '{UnstableSpeechResult}'")
        logger.info(f"   Final Transcript: '{transcript}'")
        logger.info(f"🔍 TRANSCRIPT ANALYSIS:")
        logger.info(f"   Length: {len(transcript)} characters")
        logger.info(f"   Word Count: {len(transcript.split())} words")
        logger.info(f"   Contains Emergency Keywords: {any(keyword in transcript.lower() for keyword in ['fire', 'medical', 'accident', 'police', 'ambulance', 'help', 'emergency'])}")
        
        if not transcript or len(transcript.strip()) < 5:
            logger.info(f"⚠️ INSUFFICIENT INPUT - Attempting to keep caller engaged")
            twiml_response = twilio_service.generate_emergency_retry_response()
            return Response(content=twiml_response, media_type="application/xml")
        
        # Run triage pipeline directly with Twilio transcript
        logger.info(f"🎯 STARTING TRIAGE ANALYSIS...")
        triage_result = await triage_engine.process(transcript)
        
        # DEBUG: Detailed triage logging
        logger.info(f"✅ TRIAGE COMPLETED - Call SID: {call_sid}")
        logger.info(f"📊 TRIAGE RESULTS:")
        logger.info(f"   Emergency Type: {triage_result.emergency_type.value}")
        logger.info(f"   Confidence Score: {triage_result.confidence:.2f}")
        logger.info(f"   Severity Level: {triage_result.severity_level.value}")
        logger.info(f"   Severity Score: {triage_result.severity_score:.1f}/100")
        logger.info(f"   Risk Indicators: {triage_result.risk_indicators}")
        logger.info(f"   Assigned Service: {triage_result.assigned_service.value}")
        logger.info(f"   Priority: {triage_result.priority}")
        logger.info(f"   Location: {triage_result.location}")
        logger.info(f"   Summary: {triage_result.summary}")
        
        # Generate enhanced response with safety guidance
        twiml_response = twilio_service.generate_emergency_safety_response(triage_result)
        
        logger.info(f"🎯 ENHANCED RESPONSE GENERATED - Call SID: {call_sid}")
        logger.info(f"📞 CALLER WILL RECEIVE SAFETY INSTRUCTIONS")
        
        return Response(content=twiml_response, media_type="application/xml")
        
    except Exception as e:
        logger.error(f"❌ ERROR PROCESSING EMERGENCY INPUT: {e}")
        logger.error(f"🔍 ERROR DETAILS:")
        logger.error(f"   Call SID: {CallSid}")
        logger.error(f"   SpeechResult: '{SpeechResult}'")
        logger.error(f"   Exception Type: {type(e).__name__}")
        logger.error(f"   Exception Message: {str(e)}")
        error_response = twilio_service.generate_error_response()
        return Response(content=error_response, media_type="application/xml")


@router.post("/voice/status")
async def handle_call_status(request: Request):
    """Handle call status updates from Twilio - Emergency Triage System"""
    try:
        form_data = await request.form()
        call_sid = form_data.get('CallSid', '')
        call_status = form_data.get('CallStatus', '')
        
        logger.info(f"Emergency call {call_sid} status: {call_status}")
        
        # Log call completion for audit
        if call_status in ['completed', 'failed', 'busy', 'no-answer']:
            logger.info(f"Emergency call {call_sid} ended with status: {call_status}")
        
        return Response(status_code=200)
        
    except Exception as e:
        logger.error(f"Error handling call status: {e}")
        return Response(status_code=500)
