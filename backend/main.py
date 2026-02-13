from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
<<<<<<< HEAD
from config import settings
from routes.voice import router as voice_router
=======
from backend.config import settings
from backend.routes import voice_router
from backend.routes import emergency_router, analytics_router, team_router, notifications_router
>>>>>>> 91c63386882b7ea903abf849c9707bba1e9f19a8

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
<<<<<<< HEAD
    title="RAPID-100 - Real-Time AI for Priority Incident Dispatch",
    description="Emergency triage intelligence engine for real-time incident dispatch",
=======
    title="Voice AI Phone Assistant - Professional Edition",
    description="A professional Twilio-powered voice assistant with emergency calls, analytics, team management, and notifications",
>>>>>>> 91c63386882b7ea903abf849c9707bba1e9f19a8
    version="2.0.0"
)

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
app.include_router(emergency_router, prefix="/api", tags=["emergency"])
app.include_router(analytics_router, prefix="/api", tags=["analytics"])
app.include_router(team_router, prefix="/api", tags=["team"])
app.include_router(notifications_router, prefix="/api", tags=["notifications"])


@app.get("/")
async def root():
    """Root endpoint to check if server is running"""
    return {
<<<<<<< HEAD
        "message": "RAPID-100 Emergency Triage System is running",
        "status": "active",
        "system": "Real-Time AI for Priority Incident Dispatch",
        "version": "2.0.0",
        "endpoints": {
            "emergency_webhook": "/api/voice",
            "process_emergency": "/api/voice/process",
            "call_status": "/api/voice/status"
=======
        "message": "Voice AI Phone Assistant - Professional Edition is running",
        "status": "active",
        "version": "2.0.0",
        "features": [
            "Voice calls with AI assistant",
            "Emergency call handling",
            "Analytics and reporting",
            "Team management",
            "Notifications system"
        ],
        "endpoints": {
            "voice": "/api/voice",
            "emergency": "/api/emergency",
            "analytics": "/api/analytics",
            "team": "/api/team",
            "notifications": "/api/notifications",
            "health": "/health"
>>>>>>> 91c63386882b7ea903abf849c9707bba1e9f19a8
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
<<<<<<< HEAD
        "service": "RAPID-100 Emergency Triage System",
        "version": "2.0.0",
        "system_type": "Emergency Triage Intelligence Engine"
=======
        "service": "Voice AI Phone Assistant - Professional Edition",
        "version": "2.0.0",
        "features": {
            "voice": "operational",
            "emergency": "operational", 
            "analytics": "operational",
            "team": "operational",
            "notifications": "operational"
        }
>>>>>>> 91c63386882b7ea903abf849c9707bba1e9f19a8
    }


if __name__ == "__main__":
    logger.info("Starting RAPID-100 Emergency Triage System...")
    logger.info(f"Server will run on http://{settings.HOST}:{settings.PORT}")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level="info"
    )
