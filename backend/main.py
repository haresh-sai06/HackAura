from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from datetime import datetime
from config import settings
from routes.voice import router as voice_router
from routes.calls import router as calls_router
from routes.analytics import router as analytics_router
from services.websocket_service import websocket_service
import socketio

# Configure logging with simplified output
logging.basicConfig(
    level=logging.INFO,  # Set to INFO to reduce verbosity
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('debug.log', mode='w')  # File output
    ]
)
logger = logging.getLogger(__name__)

# Set specific logger levels to INFO for cleaner output
logging.getLogger('routes.voice').setLevel(logging.INFO)
logging.getLogger('services.triage_engine').setLevel(logging.INFO)
logging.getLogger('services.classification_engine').setLevel(logging.INFO)
logging.getLogger('services.severity_engine').setLevel(logging.INFO)
logging.getLogger('services.routing_engine').setLevel(logging.INFO)
logging.getLogger('services.summary_engine').setLevel(logging.INFO)
logging.getLogger('services.twilio_service').setLevel(logging.INFO)

# Create FastAPI app
app = FastAPI(
    title="RAPID-100 - Real-Time AI for Priority Incident Dispatch",
    description="Emergency triage intelligence engine for real-time incident dispatch",
    version="2.0.0"
)

# Create Socket.IO app
sio = socketio.AsyncServer(
    cors_allowed_origins=settings.WEBSOCKET_CORS_ALLOWED_ORIGINS,
    async_mode='asgi',
    logger=settings.DEBUG,
    engineio_logger=settings.DEBUG
)

# Wrap FastAPI app with Socket.IO
socket_app = socketio.ASGIApp(sio, app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(voice_router, prefix="/api", tags=["voice"])
app.include_router(calls_router, prefix="/api", tags=["calls"])
app.include_router(analytics_router, prefix="/api", tags=["analytics"])

# Set up Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    print(f"WebSocket client connected: {sid}")
    await sio.emit('connected', {'message': 'Connected to HackAura WebSocket'}, room=sid)

@sio.event
async def disconnect(sid):
    print(f"WebSocket client disconnected: {sid}")

@sio.event
async def subscribe_analytics(sid, data):
    print(f"Client {sid} subscribed to analytics updates")
    await sio.emit('subscribed', {'type': 'analytics'}, room=sid)

@sio.event
async def subscribe_calls(sid, data):
    print(f"Client {sid} subscribed to call updates")
    await sio.emit('subscribed', {'type': 'calls'}, room=sid)

@sio.event
async def ping(sid, data):
    await sio.emit('pong', {'timestamp': datetime.utcnow().isoformat()}, room=sid)

@app.get("/")
async def root():
    """Root endpoint to check if server is running"""
    return {
        "message": "RAPID-100 Emergency Triage System is running",
        "status": "active",
        "system": "Real-Time AI for Priority Incident Dispatch",
        "version": "2.0.0",
        "features": {
            "voice_processing": True,
            "real_time_database": True,
            "websocket_support": websocket_service.sio is not None,
            "api_endpoints": True
        },
        "endpoints": {
            "emergency_webhook": "/api/voice",
            "process_emergency": "/api/voice/process",
            "call_status": "/api/voice/status",
            "calls_management": "/api/calls",
            "analytics": "/api/analytics",
            "websocket": "/socket.io",
            "health_check": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "RAPID-100 Emergency Triage System",
        "version": "2.0.0",
        "system_type": "Emergency Triage Intelligence Engine"
    }

if __name__ == "__main__":
    logger.info("Starting RAPID-100 Emergency Triage System...")
    logger.info(f"Server will run on http://{settings.HOST}:{settings.PORT}")
    
    uvicorn.run(
        "main:socket_app",  # Use the socket_app instead of app
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level="info"
    )
