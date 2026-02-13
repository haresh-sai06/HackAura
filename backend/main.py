from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from config import settings
from routes.voice import router as voice_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="RAPID-100 - Real-Time AI for Priority Incident Dispatch",
    description="Emergency triage intelligence engine for real-time incident dispatch",
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


@app.get("/")
async def root():
    """Root endpoint to check if server is running"""
    return {
        "message": "RAPID-100 Emergency Triage System is running",
        "status": "active",
        "system": "Real-Time AI for Priority Incident Dispatch",
        "version": "2.0.0",
        "endpoints": {
            "emergency_webhook": "/api/voice",
            "process_emergency": "/api/voice/process",
            "call_status": "/api/voice/status"
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
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level="info"
    )
