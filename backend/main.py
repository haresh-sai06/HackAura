from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from backend.config import settings
from backend.routes import voice_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Voice AI Phone Assistant",
    description="A Twilio-powered voice assistant using OpenAI",
    version="1.0.0"
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
        "message": "Voice AI Phone Assistant is running",
        "status": "active",
        "endpoints": {
            "voice_webhook": "/api/voice",
            "process_speech": "/api/voice/process",
            "call_status": "/api/voice/status"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Voice AI Phone Assistant",
        "version": "1.0.0"
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
