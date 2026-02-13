from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from backend.config import settings
from backend.routes import voice_router
from backend.routes import emergency_router, analytics_router, team_router, notifications_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Voice AI Phone Assistant - Professional Edition",
    description="A professional Twilio-powered voice assistant with emergency calls, analytics, team management, and notifications",
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
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Voice AI Phone Assistant - Professional Edition",
        "version": "2.0.0",
        "features": {
            "voice": "operational",
            "emergency": "operational", 
            "analytics": "operational",
            "team": "operational",
            "notifications": "operational"
        }
    }


if __name__ == "__main__":
    logger.info("Starting Voice AI Phone Assistant server...")
    logger.info(f"Server will run on http://{settings.HOST}:{settings.PORT}")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level="info"
    )
