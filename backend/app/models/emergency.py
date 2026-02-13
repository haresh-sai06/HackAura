from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
import uuid


class EmergencyType(str, Enum):
    MEDICAL = "medical"
    FIRE = "fire"
    POLICE = "police"
    ACCIDENT = "accident"
    OTHER = "other"


class EmergencyPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EmergencyStatus(str, Enum):
    PENDING = "pending"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    FALSE_ALARM = "false_alarm"


class EmergencyCall:
    def __init__(
        self,
        call_sid: str,
        emergency_type: EmergencyType,
        priority: EmergencyPriority = EmergencyPriority.MEDIUM,
        caller_location: Optional[str] = None,
        caller_phone: Optional[str] = None,
        description: Optional[str] = None,
        assigned_team_member: Optional[str] = None
    ):
        self.id = str(uuid.uuid4())
        self.call_sid = call_sid
        self.emergency_type = emergency_type
        self.priority = priority
        self.caller_location = caller_location
        self.caller_phone = caller_phone
        self.description = description
        self.assigned_team_member = assigned_team_member
        self.status = EmergencyStatus.PENDING
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.resolution_notes: Optional[str] = None
        self.escalation_level = 1
        
    def acknowledge(self, team_member_id: str):
        """Acknowledge the emergency call"""
        self.status = EmergencyStatus.ACKNOWLEDGED
        self.assigned_team_member = team_member_id
        self.updated_at = datetime.utcnow()
        
    def escalate(self):
        """Escalate the emergency to higher priority"""
        if self.escalation_level < 3:
            self.escalation_level += 1
            if self.priority == EmergencyPriority.LOW:
                self.priority = EmergencyPriority.MEDIUM
            elif self.priority == EmergencyPriority.MEDIUM:
                self.priority = EmergencyPriority.HIGH
            elif self.priority == EmergencyPriority.HIGH:
                self.priority = EmergencyPriority.CRITICAL
        self.updated_at = datetime.utcnow()
        
    def resolve(self, resolution_notes: Optional[str] = None):
        """Mark the emergency as resolved"""
        self.status = EmergencyStatus.RESOLVED
        self.resolution_notes = resolution_notes
        self.updated_at = datetime.utcnow()
        
    def mark_false_alarm(self):
        """Mark the emergency as false alarm"""
        self.status = EmergencyStatus.FALSE_ALARM
        self.updated_at = datetime.utcnow()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "call_sid": self.call_sid,
            "emergency_type": self.emergency_type.value,
            "priority": self.priority.value,
            "caller_location": self.caller_location,
            "caller_phone": self.caller_phone,
            "description": self.description,
            "assigned_team_member": self.assigned_team_member,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "resolution_notes": self.resolution_notes,
            "escalation_level": self.escalation_level
        }
