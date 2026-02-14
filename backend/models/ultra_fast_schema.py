"""
Ultra-Fast Emergency Database Schema
Minimal structure for maximum performance
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class UltraFastEmergencyCall(Base):
    """Minimal emergency call record for ultra-fast processing"""
    __tablename__ = "ultra_fast_emergency_calls"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Essential fields only
    transcript = Column(Text, nullable=False)
    category = Column(String(20), nullable=False, index=True)  # Medical/Fire/Crime/Other
    priority = Column(Integer, nullable=False, index=True)  # 1-5
    reasoning_byte = Column(String(100), nullable=False)
    
    # Performance tracking
    processing_time_ms = Column(Float, nullable=False)
    
    # Basic metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    call_sid = Column(String(100), index=True)
    from_number = Column(String(50))
    
    def to_dict(self):
        """Convert to minimal dictionary"""
        return {
            "id": self.id,
            "category": self.category,
            "priority": self.priority,
            "reasoning_byte": self.reasoning_byte,
            "processing_time_ms": self.processing_time_ms,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "call_sid": self.call_sid,
            "from_number": self.from_number
        }


class UltraFastStats(Base):
    """Performance statistics for ultra-fast service"""
    __tablename__ = "ultra_fast_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Performance metrics
    total_calls = Column(Integer, default=0)
    avg_processing_time_ms = Column(Float, default=0.0)
    min_processing_time_ms = Column(Float, default=0.0)
    max_processing_time_ms = Column(Float, default=0.0)
    
    # Category distribution
    medical_calls = Column(Integer, default=0)
    fire_calls = Column(Integer, default=0)
    crime_calls = Column(Integer, default=0)
    other_calls = Column(Integer, default=0)
    
    # Priority distribution
    priority_1_calls = Column(Integer, default=0)
    priority_2_calls = Column(Integer, default=0)
    priority_3_calls = Column(Integer, default=0)
    priority_4_calls = Column(Integer, default=0)
    priority_5_calls = Column(Integer, default=0)
