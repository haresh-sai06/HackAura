from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.app.models.notifications import Notification, NotificationManager, NotificationType, NotificationPriority, NotificationChannel, NotificationStatus
from backend.config import settings

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self):
        self.notification_manager = NotificationManager()
        self.email_config = self._get_email_config()
        self.sms_config = self._get_sms_config()
        
    def _get_email_config(self) -> Dict[str, Any]:
        """Get email configuration"""
        return {
            "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
            "smtp_port": int(os.getenv("SMTP_PORT", "587")),
            "smtp_username": os.getenv("SMTP_USERNAME", ""),
            "smtp_password": os.getenv("SMTP_PASSWORD", ""),
            "from_email": os.getenv("FROM_EMAIL", "noreply@hackaura.com")
        }
        
    def _get_sms_config(self) -> Dict[str, Any]:
        """Get SMS configuration"""
        return {
            "twilio_account_sid": settings.TWILIO_ACCOUNT_SID,
            "twilio_auth_token": settings.TWILIO_AUTH_TOKEN,
            "twilio_phone_number": settings.TWILIO_PHONE_NUMBER
        }
        
    def create_notification(
        self,
        recipient_id: str,
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.SYSTEM_ALERT,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        channels: List[NotificationChannel] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Notification:
        """Create a new notification"""
        notification = Notification(
            recipient_id=recipient_id,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            channels=channels or [NotificationChannel.IN_APP],
            data=data
        )
        
        self.notification_manager.notifications.append(notification)
        logger.info(f"Created notification: {notification.id} for {recipient_id}")
        return notification
        
    def send_notification(self, notification: Notification) -> bool:
        """Send notification through specified channels"""
        success = True
        
        for channel in notification.channels:
            try:
                if channel == NotificationChannel.EMAIL:
                    success &= self._send_email_notification(notification)
                elif channel == NotificationChannel.SMS:
                    success &= self._send_sms_notification(notification)
                elif channel == NotificationChannel.IN_APP:
                    success &= self._send_in_app_notification(notification)
                elif channel == NotificationChannel.WEBHOOK:
                    success &= self._send_webhook_notification(notification)
                    
            except Exception as e:
                logger.error(f"Failed to send notification via {channel.value}: {e}")
                success = False
                
        if success:
            notification.mark_sent()
        else:
            notification.mark_failed("Failed to send via one or more channels")
            
        return success
        
    def _send_email_notification(self, notification: Notification) -> bool:
        """Send email notification"""
        try:
            # Get recipient email (in production, would look up from user database)
            recipient_email = self._get_user_email(notification.recipient_id)
            if not recipient_email:
                logger.warning(f"No email found for user {notification.recipient_id}")
                return False
                
            msg = MIMEMultipart()
            msg['From'] = self.email_config['from_email']
            msg['To'] = recipient_email
            msg['Subject'] = notification.title
            
            # Create HTML email body
            html_body = f"""
            <html>
                <body>
                    <h2>{notification.title}</h2>
                    <p>{notification.message}</p>
                    <p><small>Priority: {notification.priority.value}</small></p>
                    <p><small>Sent: {notification.created_at.strftime('%Y-%m-%d %H:%M:%S')}</small></p>
                </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['smtp_username'], self.email_config['smtp_password'])
            text = msg.as_string()
            server.sendmail(self.email_config['from_email'], recipient_email, text)
            server.quit()
            
            logger.info(f"Email notification sent to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
            return False
            
    def _send_sms_notification(self, notification: Notification) -> bool:
        """Send SMS notification using Twilio"""
        try:
            from twilio.rest import Client
            
            # Get recipient phone number
            recipient_phone = self._get_user_phone(notification.recipient_id)
            if not recipient_phone:
                logger.warning(f"No phone number found for user {notification.recipient_id}")
                return False
                
            client = Client(self.sms_config['twilio_account_sid'], self.sms_config['twilio_auth_token'])
            
            message = client.messages.create(
                body=f"{notification.title}: {notification.message}",
                from_=self.sms_config['twilio_phone_number'],
                to=recipient_phone
            )
            
            logger.info(f"SMS notification sent to {recipient_phone}: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS notification: {e}")
            return False
            
    def _send_in_app_notification(self, notification: Notification) -> bool:
        """Send in-app notification (mark as delivered)"""
        # In a real implementation, this would use WebSocket or push notifications
        notification.mark_delivered()
        logger.info(f"In-app notification delivered to {notification.recipient_id}")
        return True
        
    def _send_webhook_notification(self, notification: Notification) -> bool:
        """Send webhook notification"""
        try:
            import requests
            
            webhook_url = os.getenv("WEBHOOK_URL", "")
            if not webhook_url:
                logger.warning("No webhook URL configured")
                return False
                
            payload = {
                "notification_id": notification.id,
                "recipient_id": notification.recipient_id,
                "title": notification.title,
                "message": notification.message,
                "type": notification.notification_type.value,
                "priority": notification.priority.value,
                "data": notification.data,
                "timestamp": notification.created_at.isoformat()
            }
            
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Webhook notification sent: {response.status_code}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send webhook notification: {e}")
            return False
            
    def _get_user_email(self, user_id: str) -> Optional[str]:
        """Get user email from team service"""
        # In production, would integrate with user database
        from backend.services.team_service import team_service
        member = team_service.get_team_member(user_id)
        return member.email if member else None
        
    def _get_user_phone(self, user_id: str) -> Optional[str]:
        """Get user phone from team service"""
        from backend.services.team_service import team_service
        member = team_service.get_team_member(user_id)
        return member.phone if member else None
        
    def get_user_notifications(
        self,
        user_id: str,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[Notification]:
        """Get notifications for a user"""
        return self.notification_manager.get_user_notifications(user_id, unread_only, limit)
        
    def mark_notification_read(self, notification_id: str, user_id: str) -> bool:
        """Mark notification as read"""
        notification = next(
            (n for n in self.notification_manager.notifications 
             if n.id == notification_id and n.recipient_id == user_id),
            None
        )
        
        if notification:
            notification.mark_read()
            logger.info(f"Notification {notification_id} marked as read")
            return True
        return False
        
    def send_bulk_notifications(
        self,
        recipient_ids: List[str],
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.SYSTEM_ALERT,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        channels: List[NotificationChannel] = None
    ) -> List[Notification]:
        """Send bulk notifications to multiple recipients"""
        notifications = []
        
        for recipient_id in recipient_ids:
            notification = self.create_notification(
                recipient_id=recipient_id,
                title=title,
                message=message,
                notification_type=notification_type,
                priority=priority,
                channels=channels
            )
            notifications.append(notification)
            
        # Send all notifications
        for notification in notifications:
            self.send_notification(notification)
            
        return notifications
        
    def process_pending_notifications(self) -> int:
        """Process all pending notifications"""
        pending = self.notification_manager.get_pending_notifications()
        processed = 0
        
        for notification in pending:
            if self.send_notification(notification):
                processed += 1
                
        logger.info(f"Processed {processed} pending notifications")
        return processed
        
    def retry_failed_notifications(self) -> int:
        """Retry failed notifications"""
        failed = self.notification_manager.get_failed_notifications()
        retried = 0
        
        for notification in failed:
            if self.send_notification(notification):
                retried += 1
                
        logger.info(f"Retried {retried} failed notifications")
        return retried
        
    def get_notification_statistics(self) -> Dict[str, Any]:
        """Get notification statistics"""
        total_notifications = len(self.notification_manager.notifications)
        
        # Count by status
        status_counts = {}
        for notification in self.notification_manager.notifications:
            status = notification.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
            
        # Count by type
        type_counts = {}
        for notification in self.notification_manager.notifications:
            notification_type = notification.notification_type.value
            type_counts[notification_type] = type_counts.get(notification_type, 0) + 1
            
        # Count by priority
        priority_counts = {}
        for notification in self.notification_manager.notifications:
            priority = notification.priority.value
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
        return {
            "total_notifications": total_notifications,
            "status_distribution": status_counts,
            "type_distribution": type_counts,
            "priority_distribution": priority_counts,
            "pending_count": len(self.notification_manager.get_pending_notifications()),
            "failed_count": len(self.notification_manager.get_failed_notifications())
        }
        
    def cleanup_old_notifications(self, days: int = 30):
        """Clean up old notifications"""
        self.notification_manager.cleanup_old_notifications(days)
        logger.info(f"Cleaned up notifications older than {days} days")


# Import required modules
import os

# Global instance
notification_service = NotificationService()
