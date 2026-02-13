import logging
import asyncio
from typing import List, Dict, Any
from datetime import datetime
import json
import socketio
from fastapi import FastAPI

from config import settings
from models.database import CallRecord, CallStatus

logger = logging.getLogger(__name__)

class WebSocketService:
    def __init__(self):
        if not settings.WEBSOCKET_ENABLED:
            logger.info("WebSocket service is disabled")
            self.sio = None
            return
            
        # Create Socket.IO server
        self.sio = socketio.AsyncServer(
            cors_allowed_origins=settings.WEBSOCKET_CORS_ALLOWED_ORIGINS,
            async_mode='asgi',
            logger=settings.DEBUG,
            engineio_logger=settings.DEBUG
        )
        
        # Register event handlers
        self.register_handlers()
        
        # Connected clients
        self.connected_clients: Dict[str, Dict[str, Any]] = {}
        
        logger.info("WebSocket service initialized")
    
    def register_handlers(self):
        """Register Socket.IO event handlers"""
        
        @self.sio.event
        async def connect(sid, environ):
            """Handle client connection"""
            client_info = {
                'sid': sid,
                'connected_at': datetime.utcnow(),
                'ip': environ.get('REMOTE_ADDR', 'unknown'),
                'user_agent': environ.get('HTTP_USER_AGENT', 'unknown')
            }
            self.connected_clients[sid] = client_info
            
            logger.info(f"WebSocket client connected: {sid}")
            await self.sio.emit('connected', {'message': 'Connected to HackAura WebSocket'}, room=sid)
            
            # Send current stats to newly connected client
            await self.broadcast_stats_update()
        
        @self.sio.event
        async def disconnect(sid):
            """Handle client disconnection"""
            if sid in self.connected_clients:
                del self.connected_clients[sid]
            logger.info(f"WebSocket client disconnected: {sid}")
        
        @self.sio.event
        async def subscribe_calls(sid, data):
            """Subscribe to call updates"""
            logger.info(f"Client {sid} subscribed to call updates")
            await self.sio.emit('subscribed', {'type': 'calls'}, room=sid)
        
        @self.sio.event
        async def subscribe_analytics(sid, data):
            """Subscribe to analytics updates"""
            logger.info(f"Client {sid} subscribed to analytics updates")
            await self.sio.emit('subscribed', {'type': 'analytics'}, room=sid)
        
        @self.sio.event
        async def ping(sid, data):
            """Handle ping for connection health check"""
            await self.sio.emit('pong', {'timestamp': datetime.utcnow().isoformat()}, room=sid)
    
    async def broadcast_new_call(self, call: CallRecord):
        """Broadcast new call to all connected clients"""
        if not self.sio:
            return
            
        try:
            call_data = {
                'id': call.id,
                'call_sid': call.call_sid,
                'from_number': call.from_number,
                'emergency_type': call.emergency_type.value,
                'severity_level': call.severity_level.value,
                'severity_score': call.severity_score,
                'status': call.status.value,
                'location_address': call.location_address,
                'transcript': call.transcript,
                'created_at': call.created_at.isoformat(),
                'confidence': call.confidence,
                'assigned_service': call.assigned_service.value,
                'priority': call.priority
            }
            
            await self.sio.emit('new_call', call_data)
            logger.info(f"Broadcasted new call {call.id} to {len(self.connected_clients)} clients")
            
        except Exception as e:
            logger.error(f"Failed to broadcast new call: {e}")
    
    async def broadcast_call_update(self, call: CallRecord):
        """Broadcast call update to all connected clients"""
        if not self.sio:
            return
            
        try:
            call_data = {
                'id': call.id,
                'call_sid': call.call_sid,
                'status': call.status.value,
                'assigned_unit': call.assigned_unit,
                'updated_at': call.updated_at.isoformat() if call.updated_at else None
            }
            
            await self.sio.emit('call_update', call_data)
            logger.info(f"Broadcasted call update {call.id} to {len(self.connected_clients)} clients")
            
        except Exception as e:
            logger.error(f"Failed to broadcast call update: {e}")
    
    async def broadcast_stats_update(self):
        """Broadcast statistics update to all connected clients"""
        if not self.sio:
            return
            
        try:
            from services.database_service import database_service
            
            # Get recent stats
            recent_calls = database_service.get_recent_calls(hours=24)
            
            stats = {
                'totalCalls': len(recent_calls),
                'pendingCalls': len([c for c in recent_calls if c.status == CallStatus.PENDING]),
                'inProgressCalls': len([c for c in recent_calls if c.status == CallStatus.IN_PROGRESS]),
                'criticalCalls': len([c for c in recent_calls if c.severity_level.value == 'Level 1']),
                'timestamp': datetime.utcnow().isoformat()
            }
            
            await self.sio.emit('stats_update', stats)
            logger.debug(f"Broadcasted stats update to {len(self.connected_clients)} clients")
            
        except Exception as e:
            logger.error(f"Failed to broadcast stats update: {e}")
    
    async def broadcast_analytics_update(self):
        """Broadcast analytics update to all connected clients"""
        if not self.sio:
            return
            
        try:
            from services.database_service import database_service
            
            analytics_data = database_service.get_analytics()
            analytics_data['timestamp'] = datetime.utcnow().isoformat()
            
            await self.sio.emit('analytics_update', analytics_data)
            logger.info(f"Broadcasted analytics update to {len(self.connected_clients)} clients")
            
        except Exception as e:
            logger.error(f"Failed to broadcast analytics update: {e}")
            # Don't raise the exception, just log it to avoid breaking the flow
    
    async def send_notification(self, notification_type: str, message: str, data: Dict[str, Any] = None):
        """Send notification to all connected clients"""
        if not self.sio:
            return
            
        try:
            notification = {
                'type': notification_type,
                'message': message,
                'data': data or {},
                'timestamp': datetime.utcnow().isoformat()
            }
            
            await self.sio.emit('notification', notification)
            logger.info(f"Sent notification: {notification_type}")
            
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
    
    def get_connected_clients_count(self) -> int:
        """Get number of connected clients"""
        return len(self.connected_clients)
    
    def get_client_info(self) -> List[Dict[str, Any]]:
        """Get information about connected clients"""
        return list(self.connected_clients.values())
    
    def mount_to_app(self, app: FastAPI):
        """Mount WebSocket server to FastAPI app"""
        if self.sio:
            app.mount('/socket.io', socketio.ASGIApp(self.sio))
            logger.info("WebSocket mounted to FastAPI app")

# Global instance
websocket_service = WebSocketService()
