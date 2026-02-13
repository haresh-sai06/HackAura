from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel
import logging

from services.database_service import database_service
from models.database import CallRecord, CallStatus, EmergencyType, SeverityLevel

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models for API responses
class CallResponse(BaseModel):
    id: int
    call_sid: str
    from_number: str
    to_number: str
    transcript: str
    emergency_type: str
    severity_level: str
    severity_score: float
    location_address: Optional[str]
    location_latitude: Optional[float]
    location_longitude: Optional[float]
    confidence: float
    risk_indicators: List[str]
    assigned_service: str
    priority: int
    summary: Optional[str]
    status: str
    assigned_unit: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    processing_time_ms: Optional[float]
    metadata: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True

class CallUpdate(BaseModel):
    status: Optional[str] = None
    assigned_unit: Optional[str] = None
    notes: Optional[str] = None

class CallAnalytics(BaseModel):
    totalCalls: int
    callsByStatus: Dict[str, int]
    callsByType: Dict[str, int]
    callsBySeverity: Dict[str, int]
    averageResponseTime: float
    resolvedCalls: int
    pendingCalls: int
    inProgressCalls: int
    dispatchedCalls: int

def call_to_dict(call):
    """Convert CallRecord to dict, handling enum types"""
    return {
        'id': call.id,
        'call_sid': call.call_sid,
        'from_number': call.from_number,
        'to_number': call.to_number,
        'transcript': call.transcript,
        'emergency_type': call.emergency_type.value if hasattr(call.emergency_type, 'value') else str(call.emergency_type),
        'severity_level': call.severity_level.value if hasattr(call.severity_level, 'value') else str(call.severity_level),
        'severity_score': call.severity_score,
        'location_address': call.location_address,
        'location_latitude': call.location_latitude,
        'location_longitude': call.location_longitude,
        'confidence': call.confidence,
        'risk_indicators': call.risk_indicators or [],
        'assigned_service': call.assigned_service.value if hasattr(call.assigned_service, 'value') else str(call.assigned_service),
        'priority': call.priority,
        'summary': call.summary,
        'status': call.status.value if hasattr(call.status, 'value') else str(call.status),
        'assigned_unit': call.assigned_unit,
        'created_at': call.created_at,
        'updated_at': call.updated_at,
        'processing_time_ms': call.processing_time_ms,
        'metadata': getattr(call, 'call_metadata', {})
    }

@router.get("/calls", response_model=List[CallResponse])
async def get_calls(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    status: Optional[str] = Query(None),
    emergency_type: Optional[str] = Query(None),
    severity_level: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None)
):
    """Get all emergency calls with optional filters"""
    try:
        filters = {}
        if status:
            filters['status'] = status
        if emergency_type:
            filters['emergency_type'] = emergency_type
        if severity_level:
            filters['severity_level'] = severity_level
        if date_from:
            filters['date_from'] = date_from
        if date_to:
            filters['date_to'] = date_to
        
        calls = database_service.get_all_calls(limit=limit, offset=offset, filters=filters)
        return [CallResponse(**call_to_dict(call)) for call in calls]
        
    except Exception as e:
        logger.error(f"Failed to get calls: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve calls")

@router.get("/calls/{call_id}", response_model=CallResponse)
async def get_call(call_id: int):
    """Get a specific call by ID"""
    try:
        call = database_service.get_call_by_id(call_id)
        if not call:
            raise HTTPException(status_code=404, detail="Call not found")
        return CallResponse(**call_to_dict(call))
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get call {call_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve call")

@router.put("/calls/{call_id}", response_model=CallResponse)
async def update_call(call_id: int, update_data: CallUpdate):
    """Update a call's status or assign a unit"""
    try:
        # Update status if provided
        if update_data.status:
            try:
                status = CallStatus(update_data.status)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid status: {update_data.status}")
            
            call = database_service.update_call_status(
                call_id, 
                status, 
                update_data.assigned_unit
            )
            
            if not call:
                raise HTTPException(status_code=404, detail="Call not found")
        
        # Add note if provided
        if update_data.notes:
            database_service.add_call_note(call_id, update_data.notes, created_by="api_user")
            call = database_service.get_call_by_id(call_id)
        
        return CallResponse(**call_to_dict(call))
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update call {call_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update call")

@router.get("/calls/{call_id}/notes")
async def get_call_notes(call_id: int):
    """Get all notes for a specific call"""
    try:
        # Verify call exists
        call = database_service.get_call_by_id(call_id)
        if not call:
            raise HTTPException(status_code=404, detail="Call not found")
        
        notes = database_service.get_call_notes(call_id)
        return [{"id": note.id, "note": note.note, "created_at": note.created_at, "created_by": note.created_by} for note in notes]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get notes for call {call_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve notes")

@router.post("/calls/{call_id}/notes")
async def add_call_note(call_id: int, note_data: Dict[str, str]):
    """Add a note to a call"""
    try:
        # Verify call exists
        call = database_service.get_call_by_id(call_id)
        if not call:
            raise HTTPException(status_code=404, detail="Call not found")
        
        note = note_data.get("note")
        if not note:
            raise HTTPException(status_code=400, detail="Note content is required")
        
        created_note = database_service.add_call_note(call_id, note, created_by="api_user")
        return {"id": created_note.id, "note": created_note.note, "created_at": created_note.created_at}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to add note to call {call_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to add note")

@router.get("/calls/recent")
async def get_recent_calls(hours: int = Query(24, ge=1, le=168)):
    """Get calls from the last N hours (default: 24 hours)"""
    try:
        calls = database_service.get_recent_calls(hours=hours)
        return [CallResponse(**call_to_dict(call)) for call in calls]
        
    except Exception as e:
        logger.error(f"Failed to get recent calls: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve recent calls")

@router.get("/stats/summary")
async def get_stats_summary():
    """Get a quick summary of current stats"""
    try:
        # Get recent calls (last 24 hours)
        recent_calls = database_service.get_recent_calls(hours=24)
        
        # Calculate summary stats
        total_calls = len(recent_calls)
        pending_calls = len([c for c in recent_calls if c.status == CallStatus.PENDING])
        in_progress_calls = len([c for c in recent_calls if c.status == CallStatus.IN_PROGRESS])
        critical_calls = len([c for c in recent_calls if c.severity_level == SeverityLevel.LEVEL_1])
        
        return {
            "totalCalls": total_calls,
            "pendingCalls": pending_calls,
            "inProgressCalls": in_progress_calls,
            "criticalCalls": critical_calls,
            "lastUpdated": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Failed to get stats summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve stats summary")
