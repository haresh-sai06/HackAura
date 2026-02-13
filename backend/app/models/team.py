from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum
import uuid


class TeamRole(str, Enum):
    ADMIN = "admin"
    SUPERVISOR = "supervisor"
    OPERATOR = "operator"
    ANALYST = "analyst"


class TeamStatus(str, Enum):
    ACTIVE = "active"
    ON_BREAK = "on_break"
    OFFLINE = "offline"
    BUSY = "busy"


class TeamMember:
    def __init__(
        self,
        name: str,
        email: str,
        phone: str,
        role: TeamRole = TeamRole.OPERATOR,
        team_id: Optional[str] = None
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.phone = phone
        self.role = role
        self.team_id = team_id
        self.status = TeamStatus.OFFLINE
        self.is_on_call = False
        self.skills = []  # List of skills (e.g., ["medical", "fire", "police"])
        self.max_concurrent_calls = 1
        self.current_calls = 0
        self.total_calls_handled = 0
        self.avg_response_time = 0
        self.rating = 5.0  # Average rating from feedback
        self.created_at = datetime.utcnow()
        self.last_active = datetime.utcnow()
        
    def update_status(self, status: TeamStatus):
        """Update team member status"""
        self.status = status
        self.last_active = datetime.utcnow()
        
    def start_call(self):
        """Increment current calls when starting a call"""
        if self.current_calls < self.max_concurrent_calls:
            self.current_calls += 1
            self.is_on_call = True
            if self.current_calls >= self.max_concurrent_calls:
                self.status = TeamStatus.BUSY
            return True
        return False
        
    def end_call(self, response_time: Optional[int] = None):
        """Decrement current calls when ending a call"""
        if self.current_calls > 0:
            self.current_calls -= 1
            self.total_calls_handled += 1
            
            if response_time:
                # Update average response time
                if self.avg_response_time == 0:
                    self.avg_response_time = response_time
                else:
                    self.avg_response_time = (self.avg_response_time + response_time) / 2
                    
            if self.current_calls == 0:
                self.is_on_call = False
                self.status = TeamStatus.ACTIVE
                
    def add_skill(self, skill: str):
        """Add a skill to the team member"""
        if skill not in self.skills:
            self.skills.append(skill)
            
    def is_available_for_call(self) -> bool:
        """Check if team member is available for new calls"""
        return (
            self.status == TeamStatus.ACTIVE and
            self.current_calls < self.max_concurrent_calls
        )
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role.value,
            "team_id": self.team_id,
            "status": self.status.value,
            "is_on_call": self.is_on_call,
            "skills": self.skills,
            "max_concurrent_calls": self.max_concurrent_calls,
            "current_calls": self.current_calls,
            "total_calls_handled": self.total_calls_handled,
            "avg_response_time": self.avg_response_time,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat()
        }


class Team:
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        specialization: Optional[str] = None
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.specialization = specialization  # e.g., "medical", "fire", "police"
        self.members = []
        self.active_calls = 0
        self.total_calls_handled = 0
        self.created_at = datetime.utcnow()
        
    def add_member(self, member: TeamMember):
        """Add a member to the team"""
        member.team_id = self.id
        self.members.append(member)
        
    def remove_member(self, member_id: str):
        """Remove a member from the team"""
        self.members = [m for m in self.members if m.id != member_id]
        
    def get_available_members(self) -> List[TeamMember]:
        """Get all available members for new calls"""
        return [member for member in self.members if member.is_available_for_call()]
        
    def get_member_by_id(self, member_id: str) -> Optional[TeamMember]:
        """Get a member by their ID"""
        for member in self.members:
            if member.id == member_id:
                return member
        return None
        
    def assign_call(self, call_sid: str) -> Optional[TeamMember]:
        """Assign a call to the best available member"""
        available_members = self.get_available_members()
        if not available_members:
            return None
            
        # Simple assignment: choose member with fewest current calls
        best_member = min(available_members, key=lambda m: m.current_calls)
        if best_member.start_call():
            self.active_calls += 1
            return best_member
        return None
        
    def get_team_stats(self) -> Dict[str, Any]:
        """Get team statistics"""
        active_members = len([m for m in self.members if m.status != TeamStatus.OFFLINE])
        available_members = len(self.get_available_members())
        
        return {
            "total_members": len(self.members),
            "active_members": active_members,
            "available_members": available_members,
            "active_calls": self.active_calls,
            "total_calls_handled": self.total_calls_handled,
            "specialization": self.specialization
        }
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "specialization": self.specialization,
            "members": [member.to_dict() for member in self.members],
            "stats": self.get_team_stats(),
            "created_at": self.created_at.isoformat()
        }
