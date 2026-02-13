from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
from backend.app.models.emergency import EmergencyCall, EmergencyType, EmergencyPriority, EmergencyStatus
from backend.app.models.team import TeamMember, Team
from backend.app.models.notifications import NotificationManager, NotificationPriority
from backend.config import settings

logger = logging.getLogger(__name__)


class EmergencyService:
    def __init__(self):
        self.active_emergencies: Dict[str, EmergencyCall] = {}
        self.emergency_history: List[EmergencyCall] = []
        self.notification_manager = NotificationManager()
        self.escalation_rules = self._initialize_escalation_rules()
        
    def _initialize_escalation_rules(self) -> Dict[str, Dict]:
        """Initialize escalation rules for different emergency types"""
        return {
            "medical": {
                "response_time_threshold": 30,  # seconds
                "auto_escalate_time": 60,      # seconds
                "required_skills": ["medical"]
            },
            "fire": {
                "response_time_threshold": 20,
                "auto_escalate_time": 45,
                "required_skills": ["fire"]
            },
            "police": {
                "response_time_threshold": 25,
                "auto_escalate_time": 50,
                "required_skills": ["police"]
            },
            "accident": {
                "response_time_threshold": 35,
                "auto_escalate_time": 70,
                "required_skills": ["medical", "police"]
            }
        }
        
    def create_emergency_call(
        self,
        call_sid: str,
        emergency_type: str,
        caller_location: Optional[str] = None,
        caller_phone: Optional[str] = None,
        description: Optional[str] = None
    ) -> EmergencyCall:
        """Create a new emergency call"""
        try:
            emergency_type_enum = EmergencyType(emergency_type.lower())
            
            # Determine priority based on type
            priority = EmergencyPriority.MEDIUM
            if emergency_type_enum in [EmergencyType.FIRE, EmergencyType.POLICE]:
                priority = EmergencyPriority.HIGH
            elif emergency_type_enum == EmergencyType.MEDICAL:
                priority = EmergencyPriority.HIGH
                
            emergency = EmergencyCall(
                call_sid=call_sid,
                emergency_type=emergency_type_enum,
                priority=priority,
                caller_location=caller_location,
                caller_phone=caller_phone,
                description=description
            )
            
            self.active_emergencies[call_sid] = emergency
            logger.info(f"Created emergency call: {emergency.id} - Type: {emergency_type}")
            
            # Trigger notifications
            self._trigger_emergency_notifications(emergency)
            
            return emergency
            
        except ValueError as e:
            logger.error(f"Invalid emergency type: {emergency_type}")
            raise ValueError(f"Invalid emergency type: {emergency_type}")
            
    def _trigger_emergency_notifications(self, emergency: EmergencyCall):
        """Trigger notifications for emergency call"""
        # This would integrate with team service to get appropriate team members
        # For now, we'll create a general notification
        notification = self.notification_manager.create_emergency_notification(
            emergency_call_id=emergency.id,
            recipient_id="emergency_team",  # This would be actual team member IDs
            emergency_type=emergency.emergency_type.value,
            priority=emergency.priority.value
        )
        logger.info(f"Created emergency notification: {notification.id}")
        
    def acknowledge_emergency(self, call_sid: str, team_member_id: str) -> bool:
        """Acknowledge an emergency call"""
        emergency = self.active_emergencies.get(call_sid)
        if not emergency:
            return False
            
        emergency.acknowledge(team_member_id)
        logger.info(f"Emergency {emergency.id} acknowledged by {team_member_id}")
        return True
        
    def escalate_emergency(self, call_sid: str) -> bool:
        """Escalate an emergency call"""
        emergency = self.active_emergencies.get(call_sid)
        if not emergency:
            return False
            
        emergency.escalate()
        logger.warning(f"Emergency {emergency.id} escalated to {emergency.priority.value}")
        
        # Trigger escalation notifications
        self._trigger_escalation_notifications(emergency)
        return True
        
    def _trigger_escalation_notifications(self, emergency: EmergencyCall):
        """Trigger notifications for emergency escalation"""
        notification = self.notification_manager.create_notification(
            recipient_id="supervisors",
            template_key="emergency_assigned",
            data={
                "emergency_type": emergency.emergency_type.value,
                "priority": emergency.priority.value,
                "escalation_level": emergency.escalation_level
            },
            priority=NotificationPriority.URGENT
        )
        
    def resolve_emergency(self, call_sid: str, resolution_notes: Optional[str] = None) -> bool:
        """Resolve an emergency call"""
        emergency = self.active_emergencies.get(call_sid)
        if not emergency:
            return False
            
        emergency.resolve(resolution_notes)
        
        # Move to history
        self.emergency_history.append(emergency)
        del self.active_emergencies[call_sid]
        
        logger.info(f"Emergency {emergency.id} resolved")
        return True
        
    def get_active_emergencies(self) -> List[EmergencyCall]:
        """Get all active emergency calls"""
        return list(self.active_emergencies.values())
        
    def get_emergency_by_call_sid(self, call_sid: str) -> Optional[EmergencyCall]:
        """Get emergency call by SID"""
        return self.active_emergencies.get(call_sid)
        
    def get_emergency_statistics(self) -> Dict[str, Any]:
        """Get emergency statistics"""
        total_emergencies = len(self.emergency_history) + len(self.active_emergencies)
        
        # Count by type
        type_counts = {}
        priority_counts = {}
        status_counts = {}
        
        all_emergencies = list(self.active_emergencies.values()) + self.emergency_history
        
        for emergency in all_emergencies:
            # Type counts
            emergency_type = emergency.emergency_type.value
            type_counts[emergency_type] = type_counts.get(emergency_type, 0) + 1
            
            # Priority counts
            priority = emergency.priority.value
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            # Status counts
            status = emergency.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
            
        # Calculate average resolution time
        resolved_emergencies = [e for e in self.emergency_history if e.status == EmergencyStatus.RESOLVED]
        avg_resolution_time = 0
        
        if resolved_emergencies:
            total_time = sum(
                (e.updated_at - e.created_at).total_seconds() 
                for e in resolved_emergencies
            )
            avg_resolution_time = total_time / len(resolved_emergencies)
            
        return {
            "total_emergencies": total_emergencies,
            "active_emergencies": len(self.active_emergencies),
            "resolved_emergencies": len(resolved_emergencies),
            "type_distribution": type_counts,
            "priority_distribution": priority_counts,
            "status_distribution": status_counts,
            "average_resolution_time_seconds": avg_resolution_time
        }
        
    def check_auto_escalation(self):
        """Check for emergencies that need auto-escalation"""
        current_time = datetime.utcnow()
        
        for emergency in self.active_emergencies.values():
            if emergency.status == EmergencyStatus.PENDING:
                time_elapsed = (current_time - emergency.created_at).total_seconds()
                rules = self.escalation_rules.get(emergency.emergency_type.value, {})
                auto_escalate_time = rules.get("auto_escalate_time", 60)
                
                if time_elapsed > auto_escalate_time:
                    self.escalate_emergency(emergency.call_sid)
                    logger.warning(f"Auto-escalated emergency {emergency.id} after {time_elapsed}s")
                    
    def detect_emergency_keywords(self, user_input: str) -> Optional[str]:
        """Detect emergency keywords in user input"""
        emergency_keywords = {
            "medical": ["help", "emergency", "medical", "doctor", "hospital", "pain", "heart", "breathing"],
            "fire": ["fire", "burning", "smoke", "flames", "explosion"],
            "police": ["police", "crime", "robbery", "theft", "assault", "danger", "weapon"],
            "accident": ["accident", "crash", "collision", "injured", "car accident"]
        }
        
        user_input_lower = user_input.lower()
        
        for emergency_type, keywords in emergency_keywords.items():
            if any(keyword in user_input_lower for keyword in keywords):
                return emergency_type
                
        return None


# Global instance
emergency_service = EmergencyService()
