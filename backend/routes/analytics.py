from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime, timedelta
import logging
from backend.services import analytics_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/analytics/dashboard")
async def get_analytics_dashboard():
    """Get comprehensive analytics dashboard data"""
    try:
        dashboard_data = analytics_service.get_dashboard_data()
        return {"success": True, "data": dashboard_data}
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/analytics/call")
async def record_call_analytics(
    call_sid: str,
    duration: int,
    is_emergency: bool = False,
    call_type: str = "standard",
    outcome: str = "completed",
    response_time: Optional[int] = None,
    team_member_id: Optional[str] = None,
    caller_location: Optional[str] = None,
    quality_score: Optional[float] = None
):
    """Record call analytics"""
    try:
        analytics_service.record_call(
            call_sid=call_sid,
            duration=duration,
            is_emergency=is_emergency,
            call_type=call_type,
            outcome=outcome,
            response_time=response_time,
            team_member_id=team_member_id,
            caller_location=caller_location,
            quality_score=quality_score
        )
        
        return {"success": True, "message": "Call analytics recorded"}
    except Exception as e:
        logger.error(f"Error recording call analytics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analytics/call/{call_sid}")
async def get_call_analytics(call_sid: str):
    """Get analytics for a specific call"""
    try:
        analytics = analytics_service.get_call_analytics(call_sid)
        if not analytics:
            raise HTTPException(status_code=404, detail="Call analytics not found")
            
        return {"success": True, "analytics": analytics}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting call analytics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analytics/calls/recent")
async def get_recent_calls(limit: int = Query(50, le=100)):
    """Get recent calls with analytics"""
    try:
        recent_calls = analytics_service.get_recent_calls(limit=limit)
        return {"success": True, "calls": recent_calls, "count": len(recent_calls)}
    except Exception as e:
        logger.error(f"Error getting recent calls: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analytics/performance")
async def get_performance_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Get performance report for date range"""
    try:
        # Parse dates if provided
        start_dt = None
        end_dt = None
        
        if start_date:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            
        report = analytics_service.get_performance_report(start_dt, end_dt)
        return {"success": True, "report": report}
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid date format")
    except Exception as e:
        logger.error(f"Error getting performance report: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analytics/export")
async def export_analytics(format: str = Query("json", regex="^(json|csv)$")):
    """Export analytics data"""
    try:
        export_data = analytics_service.export_analytics(format)
        return {"success": True, "data": export_data, "format": format}
    except Exception as e:
        logger.error(f"Error exporting analytics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analytics/summary")
async def get_analytics_summary():
    """Get analytics summary"""
    try:
        summary = analytics_service.analytics.get_summary()
        return {"success": True, "summary": summary}
    except Exception as e:
        logger.error(f"Error getting analytics summary: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analytics/daily")
async def get_daily_analytics(days: int = Query(30, le=365)):
    """Get daily analytics for specified number of days"""
    try:
        daily_stats = analytics_service.analytics.get_daily_stats(days)
        return {"success": True, "daily_stats": daily_stats, "days": days}
    except Exception as e:
        logger.error(f"Error getting daily analytics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
