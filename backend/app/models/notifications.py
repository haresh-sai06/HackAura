from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum
import uuid


class NotificationType(str, Enum):
    EMERGENCY = "emergency"
    CALL_ASSIGNED = "call_assigned"
    CALL_COMPLETED = "call_completed"
    TEAM_MEMBER_STATUS = "team_member_status"
    SYSTEM_ALERT = "system_alert"
    PERFORMANCE = "performance"


class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"
    WEBHOOK = "webhook"


class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


class Notification:
    def __init__(
        self,
        recipient_id: str,
        title: str,
        message: str,
        notification_type: NotificationType,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        channels: List[NotificationChannel] = None,
        data: Optional[Dict[str, Any]] = None
    ):
        self.id = str(uuid.uuid4())
        self.recipient_id = recipient_id
        self.title = title
        self.message = message
        self.notification_type = notification_type
        self.priority = priority
        self.channels = channels or [NotificationChannel.IN_APP]
        self.data = data or {}
        self.status = NotificationStatus.PENDING
        self.created_at = datetime.utcnow()
        self.sent_at: Optional[datetime] = None
        self.delivered_at: Optional[datetime] = None
        self.read_at: Optional[datetime] = None
        self.retry_count = 0
        self.max_retries = 3
        self.error_message: Optional[str] = None
        
    def mark_sent(self):
        """Mark notification as sent"""
        self.status = NotificationStatus.SENT
        self.sent_at = datetime.utcnow()
        
    def mark_delivered(self):
        """Mark notification as delivered"""
        self.status = NotificationStatus.DELIVERED
        self.delivered_at = datetime.utcnow()
        
    def mark_read(self):
        """Mark notification as read"""
        self.status = NotificationStatus.READ
        self.read_at = datetime.utcnow()
        
    def mark_failed(self, error_message: str):
        """Mark notification as failed"""
        self.status = NotificationStatus.FAILED
        self.error_message = error_message
        self.retry_count += 1
        
    def can_retry(self) -> bool:
        """Check if notification can be retried"""
        return self.retry_count < self.max_retries and self.status == NotificationStatus.FAILED
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "recipient_id": self.recipient_id,
            "title": self.title,
            "message": self.message,
            "notification_type": self.notification_type.value,
            "priority": self.priority.value,
            "channels": [channel.value for channel in self.channels],
            "data": self.data,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "delivered_at": self.delivered_at.isoformat() if self.delivered_at else None,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "retry_count": self.retry_count,
            "error_message": self.error_message
        }


class NotificationManager:
    def __init__(self):
        self.notifications: List[Notification] = []
        self.templates = self._initialize_templates()
        
    def _initialize_templates(self) -> Dict[str, Dict[str, str]]:
        """Initialize notification templates"""
        return {
            "emergency_assigned": {
                "title": "Emergency Call Assigned",
                "message": "You have been assigned to an emergency call: {emergency_type}. Priority: {priority}"
            },
            "call_completed": {
                "title": "Call Completed",
                "message": "Call {call_sid} has been completed. Duration: {duration}s"
            },
            "team_member_offline": {
                "title": "Team Member Offline",
                "message": "{member_name} has gone offline"
            },
            "high_call_volume": {
                "title": "High Call Volume Alert",
                "message": "Call volume is {percentage}% above normal. Consider adding more team members."
            },
            "performance_alert": {
                "title": "Performance Alert",
                "message": "Average response time is {response_time}s, which is above the threshold of {threshold}s"
            }
        }
        
    def create_notification(
        self,
        recipient_id: str,
        template_key: str,
        data: Optional[Dict[str, Any]] = None,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        channels: List[NotificationChannel] = None,
        notification_type: NotificationType = NotificationType.SYSTEM_ALERT
    ) -> Notification:
        """Create a notification from template"""
        template = self.templates.get(template_key, {
            "title": "Notification",
            "message": "You have a new notification"
        })
        
        # Format template with data
        title = template["title"].format(**(data or {}))
        message = template["message"].format(**(data or {}))
        
        notification = Notification(
            recipient_id=recipient_id,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            channels=channels,
            data=data
        )
        
        self.notifications.append(notification)
        return notification
        
    def create_emergency_notification(
        self,
        emergency_call_id: str,
        recipient_id: str,
        emergency_type: str,
        priority: str
    ) -> Notification:
        """Create emergency notification"""
        return self.create_notification(
            recipient_id=recipient_id,
            template_key="emergency_assigned",
            data={
                "emergency_type": emergency_type,
                "priority": priority,
                "emergency_call_id": emergency_call_id
            },
            priority=NotificationPriority.URGENT,
            channels=[NotificationChannel.SMS, NotificationChannel.IN_APP],
            notification_type=NotificationType.EMERGENCY
        )
        
    def get_user_notifications(
        self,
        user_id: str,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[Notification]:
        """Get notifications for a specific user"""
        notifications = [n for n in self.notifications if n.recipient_id == user_id]
        
        if unread_only:
            notifications = [n for n in notifications if n.status != NotificationStatus.READ]
            
        # Sort by created_at descending
        notifications.sort(key=lambda n: n.created_at, reverse=True)
        
        return notifications[:limit]
        
    def mark_notification_read(self, notification_id: str) -> bool:
        """Mark a notification as read"""
        for notification in self.notifications:
            if notification.id == notification_id:
                notification.mark_read()
                return True
        return False
        
    def get_pending_notifications(self) -> List[Notification]:
        """Get all pending notifications"""
        return [n for n in self.notifications if n.status == NotificationStatus.PENDING]
        
    def get_failed_notifications(self) -> List[Notification]:
        """Get all failed notifications that can be retried"""
        return [n for n in self.notifications if n.can_retry()]
        
    def cleanup_old_notifications(self, days: int = 30):
        """Clean up old notifications"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        self.notifications = [
            n for n in self.notifications 
            if n.created_at > cutoff_date or n.status == NotificationStatus.PENDING
        ]
