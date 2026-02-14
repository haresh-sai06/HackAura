from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import Response
from typing import Optional
import logging
import asyncio
import time
from services import twilio_service
from services.triage_engine import triage_engine
from services.ollama_triage_service import ollama_triage_service
from services.ollama_response_generator import ollama_response_generator
from services.hybrid_triage_service import hybrid_triage_service
from services.database_service import database_service
from services.websocket_service import websocket_service
from config import settings
from models.database import CallStatus

router = APIRouter()
logger = logging.getLogger(__name__)


async def store_result_async(result: dict, call_data: dict):
    """Store result asynchronously"""
    try:
        # Store in database using database_service
        call_record_data = {
            'call_sid': call_data.get('call_sid'),
            'from_number': call_data.get('from_number'),
            'to_number': call_data.get('to_number'),
            'transcript': call_data.get('transcript'),
            'emergency_type': result.get('category', 'OTHER'),
            'severity_level': 'LEVEL_3',
            'severity_score': 50.0,
            'assigned_service': 'AMBULANCE',
            'priority': result.get('priority', 3),
            'summary': result.get('reasoning_byte', ''),
            'confidence': result.get('confidence', 0.8),
            'status': 'PENDING',
            'processing_time_ms': result.get('processing_time_ms', 0.0)
        }
        
        database_service.create_call_record(call_record_data)
        logger.debug(f"🗄️ Result stored for {call_data.get('call_sid', 'unknown')}")
        
    except Exception as e:
        logger.error(f"❌ Async storage error: {e}")


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


@router.post("/voice/ultra-fast")
async def ultra_fast_triage(
    request: Request,
    text: Optional[str] = Form(None)
):
    """Emergency triage with Ollama AI and safety responses"""
    try:
        # Get input text
        if text:
            transcript = text
        else:
            form_data = await request.form()
            transcript = form_data.get('SpeechResult') or form_data.get('UnstableSpeechResult') or ""
        
        if not transcript or len(transcript.strip()) < 3:
            return {
                "category": "Other",
                "priority": 3,
                "reasoning_byte": "Insufficient input",
                "processing_time_ms": 0.0,
                "what_to_say": "Please describe your emergency clearly.",
                "immediate_actions": ["Stay calm", "Call for help if needed"],
                "safety_precautions": ["Keep phone available"],
                "priority_level": "MODERATE",
                "response_type": "minimal"
            }
        
        # Use hybrid triage service for conversation flow
        call_sid = form_data.get('CallSid', f"hybrid_{time.time()}")
        result = await hybrid_triage_service.process(transcript, call_sid, is_followup=False)
        
        # Store result in database
        call_data = {
            'call_sid': form_data.get('CallSid', f"ollama_{time.time()}"),
            'from_number': form_data.get('From', ''),
            'to_number': form_data.get('To', ''),
            'transcript': transcript
        }
        
        # Store asynchronously (non-blocking)
        asyncio.create_task(store_result_async(result, call_data))
        
        # Return hybrid response with complete data
        return {
            "category": result["category"],
            "priority": result["priority"],
            "reasoning_byte": result["reasoning_byte"],
            "processing_time_ms": result["processing_time_ms"],
            
            # Safety response
            "what_to_say": result["what_to_say"],
            "immediate_actions": result["immediate_actions"],
            "safety_precautions": result["safety_precautions"],
            "priority_level": result["priority_level"],
            "response_type": result["response_type"],
            "confidence": result["confidence"],
            
            # Dispatch information
            "dispatched_service": result["dispatched_service"],
            "assigned_service": result["assigned_service"],
            
            # Timestamps
            "timestamp": result["timestamp"],
            "created_at": result["created_at"],
            "call_time": result["call_time"],
            
            # Status
            "status": result["status"],
            
            # Metadata
            "classification_method": result["classification_method"],
            "safety_method": result["safety_method"],
            
            # Post-accident specific actions (if available)
            "post_accident_actions": result.get("post_accident_actions", []),
            "post_accident_precautions": result.get("post_accident_precautions", [])
        }
        
    except Exception as e:
        logger.error(f"❌ Ultra-fast triage error: {e}")
        return {
            "category": "Other",
            "priority": 3,
            "reasoning_byte": "System error",
            "processing_time_ms": 0.0,
            "what_to_say": "I'm having trouble understanding. Please stay on the line for assistance.",
            "immediate_actions": ["Stay calm"],
            "safety_precautions": ["Keep phone available"],
            "priority_level": "MODERATE",
            "response_type": "error",
            "confidence": 0.3
        }


@router.get("/voice/ultra-fast/calls")
async def get_recent_calls(limit: int = 50):
    """Get recent emergency calls for frontend"""
    try:
        # Get recent calls from database service
        session = database_service.get_session()
        from models.database import CallRecord
        
        calls = session.query(CallRecord)\
            .order_by(CallRecord.created_at.desc())\
            .limit(limit)\
            .all()
        
        # Convert to dict format with frontend compatibility
        results = []
        for call in calls:
            # Get frontend category from metadata if available
            frontend_category = 'Other'
            if call.call_metadata:
                try:
                    import json
                    metadata = json.loads(call.call_metadata)
                    frontend_category = metadata.get('frontend_category', 'Other')
                except:
                    pass
            
            # Map emergency type to frontend category if not in metadata
            if frontend_category == 'Other':
                if call.emergency_type.value == 'MEDICAL':
                    frontend_category = 'Medical'
                elif call.emergency_type.value == 'FIRE':
                    frontend_category = 'Fire'
                elif call.emergency_type.value == 'POLICE':
                    frontend_category = 'Crime'
                else:
                    frontend_category = 'Other'
            
            results.append({
                'id': call.id,
                'call_sid': call.call_sid,
                'from_number': call.from_number,
                'emergency_type': call.emergency_type.value,  # Keep original for database
                'severity_level': call.severity_level.value,
                'priority': call.priority,
                'summary': call.summary,
                'processing_time_ms': call.processing_time_ms,
                'created_at': call.created_at.isoformat() if call.created_at else None,
                'category': frontend_category  # Add frontend category
            })
        
        session.close()
        
        return {
            "success": True,
            "calls": results,
            "total": len(results)
        }
    except Exception as e:
        logger.error(f"❌ Error retrieving calls: {e}")
        return {
            "success": False,
            "calls": [],
            "total": 0,
            "error": str(e)
        }


@router.get("/voice/ultra-fast/stats")
async def get_triage_stats():
    """Get triage processing statistics"""
    try:
        # Get stats from Ollama service
        stats = ollama_triage_service.get_stats()
        
        return {
            "success": True,
            "stats": {
                'total_calls': stats['total_calls'],
                'avg_processing_time_ms': stats['avg_ms'],
                'min_ms': stats['min_ms'],
                'max_ms': stats['max_ms'],
                'service_type': 'ollama_ai'
            }
        }
    except Exception as e:
        logger.error(f"❌ Error retrieving stats: {e}")
        return {
            "success": False,
            "stats": {},
            "error": str(e)
        }


@router.post("/voice/ultra-fast/followup")
async def ultra_fast_followup(
    request: Request,
    SpeechResult: Optional[str] = Form(None),
    UnstableSpeechResult: Optional[str] = Form(None),
    CallSid: Optional[str] = Form(None)
):
    """Handle follow-up responses in emergency conversation"""
    try:
        # Get transcript and call session
        form_data = await request.form()
        transcript = SpeechResult or UnstableSpeechResult or ""
        call_sid = CallSid
        
        if not transcript or len(transcript.strip()) < 2:
            return {
                "what_to_say": "I didn't catch that. Please say yes or no.",
                "response_type": "followup_error",
                "status": "AWAITING_RESPONSE"
            }
        
        # Process as follow-up
        result = await hybrid_triage_service.process(transcript, call_sid, is_followup=True)
        
        return {
            "what_to_say": result["what_to_say"],
            "immediate_actions": result["immediate_actions"],
            "safety_precautions": result["safety_precautions"],
            "response_type": result["response_type"],
            "status": result["status"],
            "priority": result["priority"],
            "category": result["category"],
            "dispatched_service": result["dispatched_service"],
            "processing_time_ms": result["processing_time_ms"],
            "confidence": result["confidence"]
        }
        
    except Exception as e:
        logger.error(f"❌ Follow-up error: {e}")
        return {
            "what_to_say": "I'm having trouble understanding. Please stay on the line.",
            "response_type": "error",
            "status": "ERROR"
        }


@router.post("/voice/ultra-fast/voice")
async def ultra_fast_voice_response(
    request: Request,
    SpeechResult: Optional[str] = Form(None),
    UnstableSpeechResult: Optional[str] = Form(None),
    CallSid: Optional[str] = Form(None)
):
    """Generate voice response for emergency triage with conversation flow"""
    try:
        # Get transcript and call session
        form_data = await request.form()
        transcript = SpeechResult or UnstableSpeechResult or ""
        call_sid = CallSid
        
        if not transcript or len(transcript.strip()) < 2:
            # Default response for unclear input
            voice_response = "I didn't catch that. Please describe your emergency clearly."
        else:
            # Process as initial call or follow-up
            result = await hybrid_triage_service.process(transcript, call_sid, is_followup=False)
            voice_response = result["what_to_say"]
        
        # Generate TwiML response with conversation flow
        if result.get('status') == 'AWAITING_FOLLOWUP':
            # Ask danger question
            twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">{voice_response}</Say>
    <Pause length="1"/>
    <Gather input="speech" timeout="5" action="/voice/ultra-fast/followup" method="POST">
        <Say voice="alice">Is the situation more dangerous? Please say yes or no.</Say>
    </Gather>
</Response>"""
        else:
            # End call or provide final instructions
            twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">{voice_response}</Say>
    <Pause length="2"/>
    <Say voice="alice">Help is on the way. Stay safe and we will end the call when help arrives.</Say>
</Response>"""
        
        return Response(content=twiml_response, media_type="application/xml")
        
    except Exception as e:
        logger.error(f"❌ Voice response error: {e}")
        # Fallback response
        twiml_response = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">I'm having trouble understanding. Please stay on the line for assistance.</Say>
</Response>"""
        return Response(content=twiml_response, media_type="application/xml")


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
