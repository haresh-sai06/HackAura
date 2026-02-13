from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from backend.app.models.team import TeamMember, Team, TeamRole, TeamStatus
from backend.app.models.notifications import NotificationManager, NotificationType, NotificationPriority
from backend.config import settings

logger = logging.getLogger(__name__)


class TeamService:
    def __init__(self):
        self.teams: Dict[str, Team] = {}
        self.team_members: Dict[str, TeamMember] = {}
        self.notification_manager = NotificationManager()
        self._initialize_default_teams()
        
    def _initialize_default_teams(self):
        """Initialize default teams"""
        # Create emergency response teams
        medical_team = Team(
            name="Medical Response Team",
            description="Handles medical emergencies and health-related calls",
            specialization="medical"
        )
        
        fire_team = Team(
            name="Fire Response Team", 
            description="Handles fire emergencies and rescue operations",
            specialization="fire"
        )
        
        police_team = Team(
            name="Police Response Team",
            description="Handles police emergencies and security-related calls", 
            specialization="police"
        )
        
        general_team = Team(
            name="General Response Team",
            description="Handles general inquiries and non-emergency calls",
            specialization="general"
        )
        
        self.teams = {
            medical_team.id: medical_team,
            fire_team.id: fire_team,
            police_team.id: police_team,
            general_team.id: general_team
        }
        
        logger.info("Initialized default teams")
        
    def create_team_member(
        self,
        name: str,
        email: str,
        phone: str,
        role: TeamRole = TeamRole.OPERATOR,
        team_id: Optional[str] = None,
        skills: List[str] = None
    ) -> TeamMember:
        """Create a new team member"""
        team_member = TeamMember(
            name=name,
            email=email,
            phone=phone,
            role=role,
            team_id=team_id
        )
        
        if skills:
            for skill in skills:
                team_member.add_skill(skill)
                
        self.team_members[team_member.id] = team_member
        
        # Add to team if specified
        if team_id and team_id in self.teams:
            self.teams[team_id].add_member(team_member)
            
        logger.info(f"Created team member: {team_member.name} ({team_member.id})")
        return team_member
        
    def get_team_member(self, member_id: str) -> Optional[TeamMember]:
        """Get team member by ID"""
        return self.team_members.get(member_id)
        
    def get_all_team_members(self) -> List[TeamMember]:
        """Get all team members"""
        return list(self.team_members.values())
        
    def update_team_member_status(self, member_id: str, status: TeamStatus) -> bool:
        """Update team member status"""
        member = self.team_members.get(member_id)
        if not member:
            return False
            
        old_status = member.status
        member.update_status(status)
        
        # Create notification if member went offline
        if status == TeamStatus.OFFLINE and old_status != TeamStatus.OFFLINE:
            self.notification_manager.create_notification(
                recipient_id="supervisors",
                template_key="team_member_offline",
                data={"member_name": member.name},
                priority=NotificationPriority.MEDIUM,
                notification_type=NotificationType.TEAM_MEMBER_STATUS
            )
            
        logger.info(f"Updated {member.name} status to {status.value}")
        return True
        
    def assign_call_to_team_member(
        self,
        call_sid: str,
        emergency_type: Optional[str] = None,
        required_skills: List[str] = None
    ) -> Optional[TeamMember]:
        """Assign a call to the best available team member"""
        required_skills = required_skills or []
        
        # Find suitable team members
        suitable_members = []
        
        for member in self.team_members.values():
            if not member.is_available_for_call():
                continue
                
            # Check if member has required skills
            if required_skills and not any(skill in member.skills for skill in required_skills):
                continue
                
            # Check team specialization
            if emergency_type:
                member_team = self.teams.get(member.team_id) if member.team_id else None
                if member_team and member_team.specialization == emergency_type:
                    suitable_members.append(member)
                elif not member_team:  # General team members
                    suitable_members.append(member)
            else:
                suitable_members.append(member)
                
        if not suitable_members:
            logger.warning(f"No available team members for call {call_sid}")
            return None
            
        # Select best member (fewest current calls, then best response time)
        best_member = min(
            suitable_members,
            key=lambda m: (m.current_calls, m.avg_response_time)
        )
        
        # Assign call
        if best_member.start_call():
            logger.info(f"Assigned call {call_sid} to {best_member.name}")
            return best_member
            
        return None
        
    def end_call_for_team_member(self, member_id: str, call_sid: str, response_time: Optional[int] = None):
        """End a call for a team member"""
        member = self.team_members.get(member_id)
        if member:
            member.end_call(response_time)
            
            # Update team stats
            if member.team_id and member.team_id in self.teams:
                team = self.teams[member.team_id]
                team.active_calls = max(0, team.active_calls - 1)
                team.total_calls_handled += 1
                
            logger.info(f"Ended call {call_sid} for {member.name}")
            
    def get_team_by_id(self, team_id: str) -> Optional[Team]:
        """Get team by ID"""
        return self.teams.get(team_id)
        
    def get_all_teams(self) -> List[Team]:
        """Get all teams"""
        return list(self.teams.values())
        
    def get_team_statistics(self) -> Dict[str, Any]:
        """Get comprehensive team statistics"""
        total_members = len(self.team_members)
        active_members = len([
            m for m in self.team_members.values() 
            if m.status != TeamStatus.OFFLINE
        ])
        available_members = len([
            m for m in self.team_members.values() 
            if m.is_available_for_call()
        ])
        
        # Role distribution
        role_counts = {}
        for member in self.team_members.values():
            role = member.role.value
            role_counts[role] = role_counts.get(role, 0) + 1
            
        # Skill distribution
        skill_counts = {}
        for member in self.team_members.values():
            for skill in member.skills:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
                
        # Team statistics
        team_stats = {}
        for team in self.teams.values():
            team_stats[team.id] = team.get_team_stats()
            
        return {
            "total_members": total_members,
            "active_members": active_members,
            "available_members": available_members,
            "members_on_calls": len([m for m in self.team_members.values() if m.is_on_call]),
            "role_distribution": role_counts,
            "skill_distribution": skill_counts,
            "team_statistics": team_stats
        }
        
    def get_available_team_members(self, skill_filter: Optional[List[str]] = None) -> List[TeamMember]:
        """Get available team members, optionally filtered by skills"""
        available = [
            member for member in self.team_members.values()
            if member.is_available_for_call()
        ]
        
        if skill_filter:
            available = [
                member for member in available
                if any(skill in member.skills for skill in skill_filter)
            ]
            
        return available
        
    def add_skill_to_member(self, member_id: str, skill: str) -> bool:
        """Add a skill to a team member"""
        member = self.team_members.get(member_id)
        if member:
            member.add_skill(skill)
            logger.info(f"Added skill '{skill}' to {member.name}")
            return True
        return False
        
    def update_member_rating(self, member_id: str, rating: float) -> bool:
        """Update team member rating"""
        member = self.team_members.get(member_id)
        if member:
            # Simple average update (in production, would use weighted average)
            member.rating = (member.rating + rating) / 2
            logger.info(f"Updated {member.name} rating to {member.rating}")
            return True
        return False
        
    def get_performance_leaderboard(self, metric: str = "total_calls_handled", limit: int = 10) -> List[Dict[str, Any]]:
        """Get performance leaderboard"""
        members_data = []
        
        for member in self.team_members.values():
            members_data.append({
                "id": member.id,
                "name": member.name,
                "total_calls_handled": member.total_calls_handled,
                "avg_response_time": member.avg_response_time,
                "rating": member.rating,
                "current_calls": member.current_calls
            })
            
        # Sort by specified metric
        reverse_order = metric != "avg_response_time"  # Lower response time is better
        members_data.sort(key=lambda x: x[metric], reverse=reverse_order)
        
        return members_data[:limit]
        
    def check_workload_balance(self) -> Dict[str, Any]:
        """Check workload balance across team members"""
        active_members = [
            member for member in self.team_members.values()
            if member.status == TeamStatus.ACTIVE
        ]
        
        if not active_members:
            return {"status": "no_active_members", "message": "No active team members"}
            
        current_calls = [member.current_calls for member in active_members]
        avg_calls = sum(current_calls) / len(current_calls)
        max_calls = max(current_calls)
        min_calls = min(current_calls)
        
        # Check if workload is balanced (difference less than 2 calls)
        is_balanced = (max_calls - min_calls) <= 2
        
        return {
            "status": "balanced" if is_balanced else "unbalanced",
            "average_calls_per_member": avg_calls,
            "max_calls": max_calls,
            "min_calls": min_calls,
            "active_members": len(active_members),
            "recommendation": self._get_workload_recommendation(is_balanced, avg_calls, max_calls)
        }
        
    def _get_workload_recommendation(self, is_balanced: bool, avg_calls: float, max_calls: float) -> str:
        """Get workload balance recommendation"""
        if is_balanced:
            return "Workload is well balanced across team members"
        elif max_calls >= 3:
            return "Consider adding more team members or redistributing workload"
        elif avg_calls < 0.5:
            return "Consider reducing team size or increasing call volume"
        else:
            return "Some team members are overloaded, consider call redistribution"


# Global instance
team_service = TeamService()
