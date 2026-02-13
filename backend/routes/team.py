from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging
from backend.services import team_service, notification_service
from backend.app.models.team import TeamRole, TeamStatus

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/team/members")
async def create_team_member(
    name: str,
    email: str,
    phone: str,
    role: TeamRole = TeamRole.OPERATOR,
    team_id: Optional[str] = None,
    skills: Optional[List[str]] = None
):
    """Create a new team member"""
    try:
        member = team_service.create_team_member(
            name=name,
            email=email,
            phone=phone,
            role=role,
            team_id=team_id,
            skills=skills or []
        )
        
        return {"success": True, "member": member.to_dict()}
    except Exception as e:
        logger.error(f"Error creating team member: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/team/members")
async def get_all_team_members():
    """Get all team members"""
    try:
        members = team_service.get_all_team_members()
        return {
            "success": True,
            "members": [member.to_dict() for member in members],
            "count": len(members)
        }
    except Exception as e:
        logger.error(f"Error getting team members: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/team/members/{member_id}")
async def get_team_member(member_id: str):
    """Get team member by ID"""
    try:
        member = team_service.get_team_member(member_id)
        if not member:
            raise HTTPException(status_code=404, detail="Team member not found")
            
        return {"success": True, "member": member.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting team member: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/team/members/{member_id}/status")
async def update_team_member_status(member_id: str, status: TeamStatus):
    """Update team member status"""
    try:
        success = team_service.update_team_member_status(member_id, status)
        if not success:
            raise HTTPException(status_code=404, detail="Team member not found")
            
        return {"success": True, "message": "Status updated"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating team member status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/team/members/{member_id}/assign-call")
async def assign_call_to_member(
    member_id: str,
    call_sid: str,
    emergency_type: Optional[str] = None,
    required_skills: Optional[List[str]] = None
):
    """Assign a call to a specific team member"""
    try:
        member = team_service.get_team_member(member_id)
        if not member:
            raise HTTPException(status_code=404, detail="Team member not found")
            
        if not member.is_available_for_call():
            raise HTTPException(status_code=400, detail="Team member is not available")
            
        if member.start_call():
            # Send notification
            notification_service.create_notification(
                recipient_id=member_id,
                title="New Call Assigned",
                message=f"Call {call_sid} has been assigned to you",
                notification_type="call_assigned"
            )
            
            return {"success": True, "message": "Call assigned successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to assign call")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error assigning call to member: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/team/members/{member_id}/end-call")
async def end_call_for_member(
    member_id: str,
    call_sid: str,
    response_time: Optional[int] = None
):
    """End a call for a team member"""
    try:
        team_service.end_call_for_team_member(member_id, call_sid, response_time)
        return {"success": True, "message": "Call ended"}
    except Exception as e:
        logger.error(f"Error ending call for member: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/team/members/{member_id}/skills")
async def add_skill_to_member(member_id: str, skill: str):
    """Add a skill to a team member"""
    try:
        success = team_service.add_skill_to_member(member_id, skill)
        if not success:
            raise HTTPException(status_code=404, detail="Team member not found")
            
        return {"success": True, "message": "Skill added"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding skill to member: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/team/members/{member_id}/rating")
async def update_member_rating(member_id: str, rating: float):
    """Update team member rating"""
    try:
        if not (0 <= rating <= 5):
            raise HTTPException(status_code=400, detail="Rating must be between 0 and 5")
            
        success = team_service.update_member_rating(member_id, rating)
        if not success:
            raise HTTPException(status_code=404, detail="Team member not found")
            
        return {"success": True, "message": "Rating updated"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating member rating: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/teams")
async def get_all_teams():
    """Get all teams"""
    try:
        teams = team_service.get_all_teams()
        return {
            "success": True,
            "teams": [team.to_dict() for team in teams],
            "count": len(teams)
        }
    except Exception as e:
        logger.error(f"Error getting teams: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/teams/{team_id}")
async def get_team(team_id: str):
    """Get team by ID"""
    try:
        team = team_service.get_team_by_id(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
            
        return {"success": True, "team": team.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting team: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/team/statistics")
async def get_team_statistics():
    """Get team statistics"""
    try:
        stats = team_service.get_team_statistics()
        return {"success": True, "statistics": stats}
    except Exception as e:
        logger.error(f"Error getting team statistics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/team/members/available")
async def get_available_team_members(skill_filter: Optional[List[str]] = Query(None)):
    """Get available team members"""
    try:
        members = team_service.get_available_team_members(skill_filter)
        return {
            "success": True,
            "members": [member.to_dict() for member in members],
            "count": len(members)
        }
    except Exception as e:
        logger.error(f"Error getting available team members: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/team/leaderboard")
async def get_performance_leaderboard(
    metric: str = Query("total_calls_handled", regex="^(total_calls_handled|avg_response_time|rating|current_calls)$"),
    limit: int = Query(10, le=50)
):
    """Get performance leaderboard"""
    try:
        leaderboard = team_service.get_performance_leaderboard(metric, limit)
        return {"success": True, "leaderboard": leaderboard, "metric": metric}
    except Exception as e:
        logger.error(f"Error getting performance leaderboard: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/team/workload")
async def check_workload_balance():
    """Check workload balance across team members"""
    try:
        workload = team_service.check_workload_balance()
        return {"success": True, "workload": workload}
    except Exception as e:
        logger.error(f"Error checking workload balance: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/team/assign-call")
async def assign_call_to_best_member(
    call_sid: str,
    emergency_type: Optional[str] = None,
    required_skills: Optional[List[str]] = None
):
    """Assign call to best available team member"""
    try:
        member = team_service.assign_call_to_team_member(
            call_sid=call_sid,
            emergency_type=emergency_type,
            required_skills=required_skills
        )
        
        if member:
            # Send notification
            notification_service.create_notification(
                recipient_id=member.id,
                title="New Call Assigned",
                message=f"Call {call_sid} has been assigned to you",
                notification_type="call_assigned"
            )
            
            return {"success": True, "assigned_member": member.to_dict()}
        else:
            return {"success": False, "message": "No available team members"}
            
    except Exception as e:
        logger.error(f"Error assigning call: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
