from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from datetime import datetime, timedelta
import logging
from sqlalchemy.orm import Session
from sqlalchemy import text
from models.database import CallRecord, EmergencyType, SeverityLevel, CallStatus
from services.database_service import database_service
from services.websocket_service import websocket_service
# from services.analytics_service import analytics_service  # Temporarily disabled

logger = logging.getLogger(__name__)
router = APIRouter()

def get_db():
    """Dependency to get database session"""
    return database_service.get_session()


def get_calls_by_hour(calls):
    """Generate hourly call distribution data"""
    hourly_data = {hour: 0 for hour in range(24)}
    
    for call in calls:
        if call.get('created_at'):
            # Handle both datetime objects and strings
            created_at = call['created_at']
            if isinstance(created_at, str):
                try:
                    from datetime import datetime
                    created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                except:
                    continue
            
            if hasattr(created_at, 'hour'):
                hour = created_at.hour
                hourly_data[hour] += 1
    
    return [{"hour": hour, "calls": hourly_data[hour]} for hour in range(24)]


def get_calls_by_day(calls):
    """Generate weekly call distribution data"""
    day_mapping = {
        0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 
        4: "Fri", 5: "Sat", 6: "Sun"
    }
    daily_data = {day: 0 for day in day_mapping.values()}
    
    for call in calls:
        if call.get('created_at'):
            # Handle both datetime objects and strings
            created_at = call['created_at']
            if isinstance(created_at, str):
                try:
                    from datetime import datetime
                    created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                except:
                    continue
            
            if hasattr(created_at, 'weekday'):
                day_name = day_mapping[created_at.weekday()]
                daily_data[day_name] += 1
    
    return [{"day": day, "calls": daily_data[day]} for day in day_mapping.values()]


@router.get("/analytics-real")
async def get_analytics_real(db: Session = Depends(get_db)):
    """Get real analytics data - new endpoint for testing"""
    logger.info("=== REAL ANALYTICS ENDPOINT CALLED ===")
    try:
        # Get real data directly
        result = db.execute(text("""
            SELECT COUNT(*) as total_calls FROM call_records
        """))
        total_calls_result = result.fetchone()
        total_calls = total_calls_result[0] if total_calls_result else 0
        
        logger.info(f"REAL ENDPOINT: Found {total_calls} total calls in database")
        
        return {
            "totalCalls": total_calls,
            "message": "This is real data from database",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"REAL ENDPOINT Error: {e}", exc_info=True)
        return {"error": str(e)}
    finally:
        if 'db' in locals():
            db.close()


@router.get("/analytics")
async def get_analytics():
    """Get comprehensive analytics data with real-time information"""
    print("=== ANALYTICS ENDPOINT CALLED (PRINT) ===")
    logger.info("=== ANALYTICS ENDPOINT CALLED ===")
    try:
        # Use the database service which handles the data properly with robust enum handling
        analytics_data = database_service.get_analytics()
        
        # Add time-based data
        recent_calls = database_service.get_recent_calls(hours=24)
        
        # Convert calls to dict format for time functions with robust enum handling
        calls_dict = []
        for call in recent_calls:
            try:
                call_dict = {
                    'id': call.id,
                    'created_at': call.created_at,
                    'emergency_type': call.emergency_type.value if hasattr(call.emergency_type, 'value') else str(call.emergency_type),
                    'severity_level': call.severity_level.value if hasattr(call.severity_level, 'value') else str(call.severity_level),
                    'status': call.status.value if hasattr(call.status, 'value') else str(call.status),
                }
                calls_dict.append(call_dict)
            except Exception as e:
                logger.warning(f"Error processing call {call.id} for time data: {e}")
                continue
        
        # Generate time-based data
        calls_by_hour = get_calls_by_hour(calls_dict)
        calls_by_day = get_calls_by_day(calls_dict)
        
        # Combine all data
        real_data = {
            **analytics_data,
            "callsByHour": calls_by_hour,
            "callsByDay": calls_by_day,
            "lastUpdated": datetime.utcnow().isoformat()
        }
        
        print(f"Returning comprehensive real data: {real_data} (PRINT)")
        logger.info(f"Returning comprehensive real data with {real_data['totalCalls']} calls")
        return real_data
        
    except Exception as e:
        print(f"Error in analytics: {e} (PRINT)")
        logger.error(f"Error in analytics: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to fetch analytics: {str(e)}")


@router.post("/analytics/broadcast")
async def broadcast_analytics_update():
    """Trigger broadcast of analytics data to all connected WebSocket clients"""
    try:
        from main import sio
        from services.database_service import database_service
        
        analytics_data = database_service.get_analytics()
        analytics_data['timestamp'] = datetime.utcnow().isoformat()
        
        await sio.emit('analytics_update', analytics_data)
        logger.info(f"Broadcasted analytics update to all connected clients")
        
        return {
            "success": True,
            "message": "Analytics update broadcasted",
            "timestamp": datetime.utcnow().isoformat(),
            "data": analytics_data
        }
    except Exception as e:
        logger.error(f"Failed to broadcast analytics update: {e}")
        raise HTTPException(status_code=500, detail="Failed to broadcast analytics update")


@router.get("/analytics-test")
async def test_analytics_endpoint():
    """Simple test endpoint to verify analytics router is working"""
    logger.info("Analytics test endpoint called!")
    return {"message": "Analytics router is working", "timestamp": datetime.utcnow().isoformat()}


@router.get("/analytics/dashboard")
async def get_analytics_dashboard():
    """Get comprehensive analytics dashboard data"""
    try:
        # dashboard_data = analytics_service.get_dashboard_data()
        dashboard_data = {"message": "Analytics service temporarily disabled"}
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
        # analytics_service.record_call(
        #     call_sid=call_sid,
        #     duration=duration,
        #     is_emergency=is_emergency,
        #     call_type=call_type,
        #     outcome=outcome,
        #     response_time=response_time,
        #     team_member_id=team_member_id,
        #     caller_location=caller_location,
        #     quality_score=quality_score
        # )
        
        return {"success": True, "message": "Call analytics recording temporarily disabled"}
    except Exception as e:
        logger.error(f"Error recording call analytics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analytics/call/{call_sid}")
async def get_call_analytics(call_sid: str):
    """Get analytics for a specific call"""
    try:
        # analytics = analytics_service.get_call_analytics(call_sid)
        analytics = None
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
        # recent_calls = analytics_service.get_recent_calls(limit=limit)
        recent_calls = []
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
            
        # report = analytics_service.get_performance_report(start_dt, end_dt)
        report = {"message": "Performance report temporarily disabled"}
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
        # export_data = analytics_service.export_analytics(format)
        export_data = {"message": "Export temporarily disabled"}
        return {"success": True, "data": export_data, "format": format}
    except Exception as e:
        logger.error(f"Error exporting analytics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analytics/summary")
async def get_analytics_summary():
    """Get analytics summary"""
    try:
        # summary = analytics_service.analytics.get_summary()
        summary = {"message": "Summary temporarily disabled"}
        return {"success": True, "summary": summary}
    except Exception as e:
        logger.error(f"Error getting analytics summary: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analytics/daily")
async def get_daily_analytics(days: int = Query(30, le=365)):
    """Get daily analytics for specified number of days"""
    try:
        # daily_stats = analytics_service.analytics.get_daily_stats(days)
        daily_stats = {"message": "Daily stats temporarily disabled"}
        return {"success": True, "daily_stats": daily_stats, "days": days}
    except Exception as e:
        logger.error(f"Error getting daily analytics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
