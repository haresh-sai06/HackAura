from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import Response
from typing import Optional
import logging
from backend.services import gemini_service, twilio_service, emergency_service, analytics_service, team_service
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/voice")
async def handle_incoming_call(request: Request):
    """Handle incoming Twilio call webhook"""
    call_start_time = time.time()
    try:
        # Get call details
        form_data = await request.form()
        call_sid = form_data.get('CallSid', '')
        from_number = form_data.get('From', '')
        
        logger.info(f"Incoming call from {from_number}, Call SID: {call_sid}")
        
        # Try to assign to team member
        assigned_member = team_service.assign_call_to_team_member(call_sid=call_sid)
        
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
    call_start_time = time.time()
    try:
        # Get call SID
        call_sid = CallSid or ''
        
        # Use the stable speech result if available, otherwise use unstable
        user_input = SpeechResult or UnstableSpeechResult or ""
        
        logger.info(f"Processing speech input for call {call_sid}: {user_input}")
        
        if not user_input:
            # No speech detected, generate goodbye response
            twiml_response = twilio_service.generate_goodbye_response()
            
            # Record call analytics
            response_time = int((time.time() - call_start_time) * 1000)
            analytics_service.record_call(
                call_sid=call_sid,
                duration=0,  # Will be updated when call ends
                is_emergency=False,
                call_type="no_input",
                outcome="no_input",
                response_time=response_time
            )
            
            return Response(content=twiml_response, media_type="application/xml")
        
        # Check for emergency keywords
        emergency_type = emergency_service.detect_emergency_keywords(user_input)
        is_emergency = emergency_type is not None
        
        if is_emergency:
            # Create emergency call
            emergency = emergency_service.create_emergency_call(
                call_sid=call_sid,
                emergency_type=emergency_type,
                description=f"Detected from user input: {user_input}"
            )
            
            # Assign to specialized team member
            required_skills = [emergency_type] if emergency_type != "other" else []
            assigned_member = team_service.assign_call_to_team_member(
                call_sid=call_sid,
                emergency_type=emergency_type,
                required_skills=required_skills
            )
            
            if assigned_member:
                emergency_service.acknowledge_emergency(call_sid, assigned_member.id)
        
        # Check for goodbye keywords
        goodbye_keywords = ['goodbye', 'bye', 'thank you', 'thanks', 'that\'s all', 'done', 'finish']
        if any(keyword in user_input.lower() for keyword in goodbye_keywords):
            twiml_response = twilio_service.generate_goodbye_response()
            
            # Record call analytics
            response_time = int((time.time() - call_start_time) * 1000)
            analytics_service.record_call(
                call_sid=call_sid,
                duration=0,
                is_emergency=is_emergency,
                call_type="standard",
                outcome="completed",
                response_time=response_time
            )
            
            return Response(content=twiml_response, media_type="application/xml")
        
        # Generate AI response
        ai_response = await gemini_service.generate_response(call_sid, user_input)
        logger.info(f"AI Response for call {call_sid}: {ai_response}")
        
        # Record call analytics
        response_time = int((time.time() - call_start_time) * 1000)
        analytics_service.record_call(
            call_sid=call_sid,
            duration=0,  # Will be updated when call ends
            is_emergency=is_emergency,
            call_type="emergency" if is_emergency else "standard",
            outcome="processing",
            response_time=response_time
        )
        
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
        call_duration = form_data.get('CallDuration', '0')
        
        logger.info(f"Call {call_sid} status: {call_status}, duration: {call_duration}s")
        
        # Clear conversation history when call ends
        if call_status in ['completed', 'failed', 'busy', 'no-answer']:
            gemini_service.clear_conversation(call_sid)
            logger.info(f"Cleared conversation history for call {call_sid}")
            
            # End call for assigned team member
            from backend.services.team_service import team_service
            for member_id, member in team_service.team_members.items():
                if member.is_on_call and member.current_calls > 0:
                    team_service.end_call_for_team_member(member_id, call_sid)
                    break
            
            # Record final call analytics
            try:
                duration = int(call_duration)
                analytics_service.record_call(
                    call_sid=call_sid,
                    duration=duration,
                    is_emergency=False,  # This would be tracked during the call
                    call_type="standard",
                    outcome=call_status,
                    response_time=None  # Already recorded during processing
                )
            except (ValueError, TypeError):
                logger.warning(f"Invalid call duration: {call_duration}")
        
        return Response(status_code=200)
        
    except Exception as e:
        logger.error(f"Error handling call status: {e}")
        return Response(status_code=500)
