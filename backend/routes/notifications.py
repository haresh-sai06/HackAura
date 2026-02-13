from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging
from backend.services import notification_service
from backend.app.models.notifications import NotificationType, NotificationPriority, NotificationChannel

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/notifications")
async def create_notification(
    recipient_id: str,
    title: str,
    message: str,
    notification_type: NotificationType = NotificationType.SYSTEM_ALERT,
    priority: NotificationPriority = NotificationPriority.MEDIUM,
    channels: Optional[List[NotificationChannel]] = None,
    data: Optional[dict] = None
):
    """Create a new notification"""
    try:
        notification = notification_service.create_notification(
            recipient_id=recipient_id,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            channels=channels or [NotificationChannel.IN_APP],
            data=data
        )
        
        return {"success": True, "notification": notification.to_dict()}
    except Exception as e:
        logger.error(f"Error creating notification: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/notifications/send/{notification_id}")
async def send_notification(notification_id: str):
    """Send a notification"""
    try:
        notification = None
        for n in notification_service.notification_manager.notifications:
            if n.id == notification_id:
                notification = n
                break
                
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
            
        success = notification_service.send_notification(notification)
        
        return {"success": success, "notification": notification.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/notifications/user/{user_id}")
async def get_user_notifications(
    user_id: str,
    unread_only: bool = Query(False),
    limit: int = Query(50, le=100)
):
    """Get notifications for a specific user"""
    try:
        notifications = notification_service.get_user_notifications(
            user_id=user_id,
            unread_only=unread_only,
            limit=limit
        )
        
        return {
            "success": True,
            "notifications": [n.to_dict() for n in notifications],
            "count": len(notifications)
        }
    except Exception as e:
        logger.error(f"Error getting user notifications: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: str, user_id: str):
    """Mark notification as read"""
    try:
        success = notification_service.mark_notification_read(notification_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Notification not found")
            
        return {"success": True, "message": "Notification marked as read"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking notification as read: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/notifications/bulk")
async def send_bulk_notifications(
    recipient_ids: List[str],
    title: str,
    message: str,
    notification_type: NotificationType = NotificationType.SYSTEM_ALERT,
    priority: NotificationPriority = NotificationPriority.MEDIUM,
    channels: Optional[List[NotificationChannel]] = None
):
    """Send bulk notifications to multiple recipients"""
    try:
        notifications = notification_service.send_bulk_notifications(
            recipient_ids=recipient_ids,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            channels=channels
        )
        
        return {
            "success": True,
            "notifications_sent": len(notifications),
            "notifications": [n.to_dict() for n in notifications]
        }
    except Exception as e:
        logger.error(f"Error sending bulk notifications: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/notifications/process-pending")
async def process_pending_notifications():
    """Process all pending notifications"""
    try:
        processed = notification_service.process_pending_notifications()
        return {"success": True, "processed_count": processed}
    except Exception as e:
        logger.error(f"Error processing pending notifications: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/notifications/retry-failed")
async def retry_failed_notifications():
    """Retry failed notifications"""
    try:
        retried = notification_service.retry_failed_notifications()
        return {"success": True, "retried_count": retried}
    except Exception as e:
        logger.error(f"Error retrying failed notifications: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/notifications/statistics")
async def get_notification_statistics():
    """Get notification statistics"""
    try:
        stats = notification_service.get_notification_statistics()
        return {"success": True, "statistics": stats}
    except Exception as e:
        logger.error(f"Error getting notification statistics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/notifications/cleanup")
async def cleanup_old_notifications(days: int = Query(30, le=365)):
    """Clean up old notifications"""
    try:
        notification_service.cleanup_old_notifications(days)
        return {"success": True, "message": f"Cleaned up notifications older than {days} days"}
    except Exception as e:
        logger.error(f"Error cleaning up notifications: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/notifications/emergency")
async def create_emergency_notification(
    emergency_call_id: str,
    recipient_id: str,
    emergency_type: str,
    priority: str
):
    """Create emergency notification"""
    try:
        notification = notification_service.notification_manager.create_emergency_notification(
            emergency_call_id=emergency_call_id,
            recipient_id=recipient_id,
            emergency_type=emergency_type,
            priority=priority
        )
        
        # Send the notification immediately
        notification_service.send_notification(notification)
        
        return {"success": True, "notification": notification.to_dict()}
    except Exception as e:
        logger.error(f"Error creating emergency notification: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/notifications/team-alert")
async def create_team_alert(
    title: str,
    message: str,
    team_id: Optional[str] = None,
    priority: NotificationPriority = NotificationPriority.MEDIUM
):
    """Create team alert notification"""
    try:
        from backend.services.team_service import team_service
        
        # Get recipients
        if team_id:
            team = team_service.get_team_by_id(team_id)
            if not team:
                raise HTTPException(status_code=404, detail="Team not found")
            recipient_ids = [member.id for member in team.members]
        else:
            # Send to all team members
            members = team_service.get_all_team_members()
            recipient_ids = [member.id for member in members]
            
        if not recipient_ids:
            return {"success": False, "message": "No recipients found"}
            
        notifications = notification_service.send_bulk_notifications(
            recipient_ids=recipient_ids,
            title=title,
            message=message,
            notification_type=NotificationType.SYSTEM_ALERT,
            priority=priority,
            channels=[NotificationChannel.IN_APP, NotificationChannel.EMAIL]
        )
        
        return {
            "success": True,
            "notifications_sent": len(notifications),
            "recipients": len(recipient_ids)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating team alert: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
