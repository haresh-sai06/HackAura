from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
import logging
from backend.services import emergency_service, team_service, notification_service
from backend.app.models.emergency import EmergencyType, EmergencyPriority, EmergencyStatus

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/emergency")
async def create_emergency_call(
    call_sid: str,
    emergency_type: str,
    caller_location: Optional[str] = None,
    caller_phone: Optional[str] = None,
    description: Optional[str] = None
):
    """Create a new emergency call"""
    try:
        emergency = emergency_service.create_emergency_call(
            call_sid=call_sid,
            emergency_type=emergency_type,
            caller_location=caller_location,
            caller_phone=caller_phone,
            description=description
        )
        
        # Try to assign to team member
        required_skills = [emergency_type] if emergency_type != "other" else []
        assigned_member = team_service.assign_call_to_team_member(
            call_sid=call_sid,
            emergency_type=emergency_type,
            required_skills=required_skills
        )
        
        if assigned_member:
            emergency_service.acknowledge_emergency(call_sid, assigned_member.id)
            
            # Send notification to assigned member
            notification_service.create_notification(
                recipient_id=assigned_member.id,
                title="Emergency Call Assigned",
                message=f"Emergency call {call_sid} assigned to you. Type: {emergency_type}",
                notification_type="emergency",
                priority="urgent"
            )
        
        return {
            "success": True,
            "emergency": emergency.to_dict(),
            "assigned_member": assigned_member.to_dict() if assigned_member else None
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating emergency call: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/emergency/active")
async def get_active_emergencies():
    """Get all active emergency calls"""
    try:
        emergencies = emergency_service.get_active_emergencies()
        return {
            "success": True,
            "emergencies": [emergency.to_dict() for emergency in emergencies],
            "count": len(emergencies)
        }
    except Exception as e:
        logger.error(f"Error getting active emergencies: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/emergency/{call_sid}")
async def get_emergency_by_call_sid(call_sid: str):
    """Get emergency call by SID"""
    try:
        emergency = emergency_service.get_emergency_by_call_sid(call_sid)
        if not emergency:
            raise HTTPException(status_code=404, detail="Emergency call not found")
            
        return {
            "success": True,
            "emergency": emergency.to_dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting emergency call: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/emergency/{call_sid}/acknowledge")
async def acknowledge_emergency(call_sid: str, team_member_id: str):
    """Acknowledge an emergency call"""
    try:
        success = emergency_service.acknowledge_emergency(call_sid, team_member_id)
        if not success:
            raise HTTPException(status_code=404, detail="Emergency call not found")
            
        return {"success": True, "message": "Emergency acknowledged"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error acknowledging emergency: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/emergency/{call_sid}/escalate")
async def escalate_emergency(call_sid: str):
    """Escalate an emergency call"""
    try:
        success = emergency_service.escalate_emergency(call_sid)
        if not success:
            raise HTTPException(status_code=404, detail="Emergency call not found")
            
        return {"success": True, "message": "Emergency escalated"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error escalating emergency: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/emergency/{call_sid}/resolve")
async def resolve_emergency(call_sid: str, resolution_notes: Optional[str] = None):
    """Resolve an emergency call"""
    try:
        success = emergency_service.resolve_emergency(call_sid, resolution_notes)
        if not success:
            raise HTTPException(status_code=404, detail="Emergency call not found")
            
        # End call for assigned team member
        emergency = emergency_service.get_emergency_by_call_sid(call_sid)
        if emergency and emergency.assigned_team_member:
            team_service.end_call_for_team_member(emergency.assigned_team_member, call_sid)
            
        return {"success": True, "message": "Emergency resolved"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resolving emergency: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/emergency/statistics")
async def get_emergency_statistics():
    """Get emergency statistics"""
    try:
        stats = emergency_service.get_emergency_statistics()
        return {"success": True, "statistics": stats}
    except Exception as e:
        logger.error(f"Error getting emergency statistics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/emergency/detect")
async def detect_emergency_in_call(call_sid: str, user_input: str):
    """Detect emergency keywords in call input"""
    try:
        emergency_type = emergency_service.detect_emergency_keywords(user_input)
        
        if emergency_type:
            # Create emergency call
            emergency = emergency_service.create_emergency_call(
                call_sid=call_sid,
                emergency_type=emergency_type,
                description=f"Detected from user input: {user_input}"
            )
            
            return {
                "success": True,
                "emergency_detected": True,
                "emergency_type": emergency_type,
                "emergency": emergency.to_dict()
            }
        else:
            return {
                "success": True,
                "emergency_detected": False
            }
            
    except Exception as e:
        logger.error(f"Error detecting emergency: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
