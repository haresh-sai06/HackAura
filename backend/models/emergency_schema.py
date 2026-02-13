from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class EmergencyType(str, Enum):
    MEDICAL = "MEDICAL"
    FIRE = "FIRE"
    POLICE = "POLICE"
    ACCIDENT = "ACCIDENT"
    MENTAL_HEALTH = "MENTAL_HEALTH"
    OTHER = "OTHER"


class SeverityLevel(str, Enum):
    LEVEL_1 = "LEVEL_1"  # Critical
    LEVEL_2 = "LEVEL_2"  # High
    LEVEL_3 = "LEVEL_3"  # Moderate
    LEVEL_4 = "LEVEL_4"  # Low


class EmergencyService(str, Enum):
    AMBULANCE = "AMBULANCE"
    FIRE_DEPARTMENT = "FIRE_DEPARTMENT"
    POLICE = "POLICE"
    CRISIS_RESPONSE = "CRISIS_RESPONSE"
    MULTIPLE = "MULTIPLE_SERVICES"


class ClassificationResult(BaseModel):
    emergency_type: EmergencyType
    confidence: float = Field(ge=0.0, le=1.0)


class SeverityResult(BaseModel):
    level: SeverityLevel
    score: float = Field(ge=0.0, le=100.0)
    risk_indicators: List[str]


class RoutingResult(BaseModel):
    assigned_service: EmergencyService
    priority: int = Field(ge=1, le=10)


class TriageResult(BaseModel):
    transcript: str
    emergency_type: EmergencyType
    severity_level: SeverityLevel
    severity_score: float
    risk_indicators: List[str]
    assigned_service: EmergencyService
    priority: int = Field(ge=1, le=10)
    location: Optional[str] = None
    summary: str
    confidence: float = Field(ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    processing_time_ms: Optional[float] = None


class CallMetadata(BaseModel):
    call_sid: str
    from_number: str
    recording_url: Optional[str] = None
    call_timestamp: datetime = Field(default_factory=datetime.utcnow)


class EmergencyRequest(BaseModel):
    call_metadata: CallMetadata
    transcript: Optional[str] = None
    recording_url: Optional[str] = None
