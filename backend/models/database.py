from sqlalchemy import Column, Integer, String, DateTime, Text, Float, JSON, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

class EmergencyType(str, enum.Enum):
    MEDICAL = "MEDICAL"
    FIRE = "FIRE"
    POLICE = "POLICE"
    ACCIDENT = "ACCIDENT"
    MENTAL_HEALTH = "MENTAL_HEALTH"
    NATURAL_DISASTER = "NATURAL_DISASTER"
    OTHER = "OTHER"

class SeverityLevel(str, enum.Enum):
    LEVEL_1 = "LEVEL_1"  # Critical
    LEVEL_2 = "LEVEL_2"  # High
    LEVEL_3 = "LEVEL_3"  # Moderate
    LEVEL_4 = "LEVEL_4"  # Low

class CallStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    DISPATCHED = "DISPATCHED"
    RESOLVED = "RESOLVED"
    CANCELLED = "CANCELLED"

class EmergencyService(str, enum.Enum):
    AMBULANCE = "AMBULANCE"
    FIRE_DEPARTMENT = "FIRE_DEPARTMENT"
    POLICE = "POLICE"
    MULTIPLE_SERVICES = "MULTIPLE_SERVICES"
    CRISIS_RESPONSE = "CRISIS_RESPONSE"

class CallRecord(Base):
    __tablename__ = "call_records"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Call information
    call_sid = Column(String(100), unique=True, index=True, nullable=False)
    from_number = Column(String(20), nullable=False)
    to_number = Column(String(20), nullable=False)
    
    # Emergency details
    transcript = Column(Text, nullable=False)
    emergency_type = Column(Enum(EmergencyType), nullable=False)
    severity_level = Column(Enum(SeverityLevel), nullable=False)
    severity_score = Column(Float, nullable=False)
    
    # Location information
    location_address = Column(String(500))
    location_latitude = Column(Float)
    location_longitude = Column(Float)
    
    # Triage information
    confidence = Column(Float, nullable=False)
    risk_indicators = Column(JSON)
    assigned_service = Column(Enum(EmergencyService), nullable=False)
    priority = Column(Integer, nullable=False)
    summary = Column(Text)
    
    # Status tracking
    status = Column(Enum(CallStatus), default=CallStatus.PENDING, nullable=False)
    assigned_unit = Column(String(50))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    processing_time_ms = Column(Float)
    
    # Additional metadata
    call_metadata = Column(JSON)

class CallNote(Base):
    __tablename__ = "call_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(Integer, nullable=False)
    note = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(String(100))
    
    # Foreign key relationship
    # call = relationship("CallRecord", back_populates="notes")

class Analytics(Base):
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Call counts
    total_calls = Column(Integer, default=0)
    pending_calls = Column(Integer, default=0)
    in_progress_calls = Column(Integer, default=0)
    dispatched_calls = Column(Integer, default=0)
    resolved_calls = Column(Integer, default=0)
    cancelled_calls = Column(Integer, default=0)
    
    # Emergency type breakdown
    medical_calls = Column(Integer, default=0)
    fire_calls = Column(Integer, default=0)
    police_calls = Column(Integer, default=0)
    accident_calls = Column(Integer, default=0)
    mental_health_calls = Column(Integer, default=0)
    other_calls = Column(Integer, default=0)
    
    # Severity breakdown
    level_1_calls = Column(Integer, default=0)
    level_2_calls = Column(Integer, default=0)
    level_3_calls = Column(Integer, default=0)
    level_4_calls = Column(Integer, default=0)
    
    # Performance metrics
    average_response_time = Column(Float, default=0.0)
    average_processing_time = Column(Float, default=0.0)
    
    # Additional metrics
    analytics_metadata = Column(JSON)

# Add relationship to CallRecord
CallRecord.notes = []  # This will be properly set up with relationships
