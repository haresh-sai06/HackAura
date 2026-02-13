import logging
from sqlalchemy import create_engine, desc, and_, or_, func
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from models.database import Base, CallRecord, CallNote, Analytics, EmergencyType, SeverityLevel, CallStatus, EmergencyService
from config import settings
from utils.enum_utils import normalize_emergency_type, normalize_severity_level, normalize_call_status, normalize_emergency_service

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.engine = create_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,
            connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.create_tables()
    
    def create_tables(self):
        """Create all database tables"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
    
    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()
    
    def create_call_record(self, call_data: Dict[str, Any]) -> CallRecord:
        """Create a new call record with robust enum handling"""
        session = self.get_session()
        try:
            # Normalize enum values with case-insensitive support
            emergency_type = normalize_emergency_type(call_data.get('emergency_type', 'OTHER'))
            severity_level = normalize_severity_level(call_data.get('severity_level', 'LEVEL_3'))
            status = normalize_call_status(call_data.get('status', 'PENDING'))
            assigned_service = normalize_emergency_service(call_data.get('assigned_service', 'POLICE'))
            
            call_record = CallRecord(
                call_sid=call_data.get('call_sid'),
                from_number=call_data.get('from_number'),
                to_number=call_data.get('to_number'),
                transcript=call_data.get('transcript'),
                emergency_type=emergency_type,
                severity_level=severity_level,
                severity_score=call_data.get('severity_score'),
                location_address=call_data.get('location_address'),
                location_latitude=call_data.get('location_latitude'),
                location_longitude=call_data.get('location_longitude'),
                confidence=call_data.get('confidence'),
                risk_indicators=call_data.get('risk_indicators', []),
                assigned_service=assigned_service,
                priority=call_data.get('priority'),
                summary=call_data.get('summary'),
                status=status,
                assigned_unit=call_data.get('assigned_unit'),
                processing_time_ms=call_data.get('processing_time_ms'),
                call_metadata=call_data.get('metadata', {})
            )
            
            session.add(call_record)
            session.commit()
            session.refresh(call_record)
            
            logger.info(f"Created call record: {call_record.id} - {call_record.emergency_type.value}")
            return call_record
            
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Failed to create call record: {e}")
            raise
        finally:
            session.close()
    
    def get_call_by_sid(self, call_sid: str) -> Optional[CallRecord]:
        """Get call record by call SID"""
        session = self.get_session()
        try:
            return session.query(CallRecord).filter(CallRecord.call_sid == call_sid).first()
        except SQLAlchemyError as e:
            logger.error(f"Failed to get call by SID: {e}")
            return None
        finally:
            session.close()
    
    def get_call_by_id(self, call_id: int) -> Optional[CallRecord]:
        """Get call record by ID"""
        session = self.get_session()
        try:
            return session.query(CallRecord).filter(CallRecord.id == call_id).first()
        except SQLAlchemyError as e:
            logger.error(f"Failed to get call by ID: {e}")
            return None
        finally:
            session.close()
    
    def get_all_calls(self, limit: int = 100, offset: int = 0, filters: Optional[Dict[str, Any]] = None) -> List[CallRecord]:
        """Get all call records with optional filters"""
        session = self.get_session()
        try:
            query = session.query(CallRecord)
            
            # Apply filters
            if filters:
                if filters.get('status'):
                    query = query.filter(CallRecord.status == filters['status'])
                if filters.get('emergency_type'):
                    query = query.filter(CallRecord.emergency_type == filters['emergency_type'])
                if filters.get('severity_level'):
                    query = query.filter(CallRecord.severity_level == filters['severity_level'])
                if filters.get('date_from'):
                    query = query.filter(CallRecord.created_at >= filters['date_from'])
                if filters.get('date_to'):
                    query = query.filter(CallRecord.created_at <= filters['date_to'])
            
            # Order by most recent first and apply pagination
            return query.order_by(desc(CallRecord.created_at)).offset(offset).limit(limit).all()
            
        except SQLAlchemyError as e:
            logger.error(f"Failed to get calls: {e}")
            return []
        finally:
            session.close()
    
    def update_call_status(self, call_id: int, status: CallStatus, assigned_unit: Optional[str] = None) -> Optional[CallRecord]:
        """Update call status"""
        session = self.get_session()
        try:
            call_record = session.query(CallRecord).filter(CallRecord.id == call_id).first()
            if call_record:
                call_record.status = status
                if assigned_unit:
                    call_record.assigned_unit = assigned_unit
                call_record.updated_at = datetime.utcnow()
                session.commit()
                session.refresh(call_record)
                logger.info(f"Updated call {call_id} status to {status}")
                return call_record
            return None
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Failed to update call status: {e}")
            return None
        finally:
            session.close()
    
    def add_call_note(self, call_id: int, note: str, created_by: Optional[str] = None) -> CallNote:
        """Add a note to a call record"""
        session = self.get_session()
        try:
            call_note = CallNote(
                call_id=call_id,
                note=note,
                created_by=created_by
            )
            
            session.add(call_note)
            session.commit()
            session.refresh(call_note)
            
            logger.info(f"Added note to call {call_id}")
            return call_note
            
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Failed to add call note: {e}")
            raise
        finally:
            session.close()
    
    def get_call_notes(self, call_id: int) -> List[CallNote]:
        """Get all notes for a call"""
        session = self.get_session()
        try:
            return session.query(CallNote).filter(CallNote.call_id == call_id).order_by(desc(CallNote.created_at)).all()
        except SQLAlchemyError as e:
            logger.error(f"Failed to get call notes: {e}")
            return []
        finally:
            session.close()
    
    def get_analytics(self, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None) -> Dict[str, Any]:
        """Get analytics data with robust enum handling"""
        session = self.get_session()
        try:
            query = session.query(CallRecord)
            
            if date_from:
                query = query.filter(CallRecord.created_at >= date_from)
            if date_to:
                query = query.filter(CallRecord.created_at <= date_to)
            
            calls = query.all()
            
            # Calculate analytics
            total_calls = len(calls)
            
            # Initialize counters
            calls_by_status = {
                'pending': 0, 'in_progress': 0, 'dispatched': 0, 'resolved': 0, 'cancelled': 0
            }
            calls_by_type = {
                'medical': 0, 'fire': 0, 'police': 0, 'accident': 0, 'mental_health': 0, 'other': 0
            }
            calls_by_severity = {
                'low': 0, 'medium': 0, 'high': 0, 'critical': 0
            }
            
            # Count by status using robust enum handling
            for call in calls:
                try:
                    status_key = call.status.value.lower() if call.status else 'pending'
                    if status_key in calls_by_status:
                        calls_by_status[status_key] += 1
                except Exception as e:
                    logger.warning(f"Error processing status for call {call.id}: {e}")
            
            # Count by emergency type using robust enum handling
            for call in calls:
                try:
                    if hasattr(call.emergency_type, 'value'):
                        type_key = call.emergency_type.value.lower()
                    else:
                        type_key = str(call.emergency_type).lower()
                    
                    # Map to our categories
                    if 'medical' in type_key:
                        calls_by_type['medical'] += 1
                    elif 'fire' in type_key:
                        calls_by_type['fire'] += 1
                    elif 'police' in type_key:
                        calls_by_type['police'] += 1
                    elif 'accident' in type_key:
                        calls_by_type['accident'] += 1
                    elif 'mental' in type_key:
                        calls_by_type['mental_health'] += 1
                    else:
                        calls_by_type['other'] += 1
                except Exception as e:
                    logger.warning(f"Error processing emergency type for call {call.id}: {e}")
            
            # Count by severity using robust enum handling
            for call in calls:
                try:
                    if hasattr(call.severity_level, 'value'):
                        severity_key = call.severity_level.value.lower()
                    else:
                        severity_key = str(call.severity_level).lower()
                    
                    # Map to our categories
                    if 'level_1' in severity_key or 'critical' in severity_key:
                        calls_by_severity['critical'] += 1
                    elif 'level_2' in severity_key or 'high' in severity_key:
                        calls_by_severity['high'] += 1
                    elif 'level_3' in severity_key or 'moderate' in severity_key or 'medium' in severity_key:
                        calls_by_severity['medium'] += 1
                    elif 'level_4' in severity_key or 'low' in severity_key:
                        calls_by_severity['low'] += 1
                except Exception as e:
                    logger.warning(f"Error processing severity level for call {call.id}: {e}")
            
            # Calculate average response/processing times
            avg_processing_time = sum(c.processing_time_ms or 0 for c in calls) / total_calls if total_calls > 0 else 0
            
            return {
                'totalCalls': total_calls,
                'callsByStatus': calls_by_status,
                'callsByType': calls_by_type,
                'callsBySeverity': calls_by_severity,
                'averageResponseTime': avg_processing_time / 1000,  # Convert to seconds
                'resolvedCalls': calls_by_status.get('resolved', 0),
                'pendingCalls': calls_by_status.get('pending', 0),
                'inProgressCalls': calls_by_status.get('in_progress', 0),
                'dispatchedCalls': calls_by_status.get('dispatched', 0),
            }
            
        except SQLAlchemyError as e:
            logger.error(f"Failed to get analytics: {e}")
            return {}
        finally:
            session.close()
    
    def get_recent_calls(self, hours: int = 24) -> List[CallRecord]:
        """Get calls from the last N hours"""
        session = self.get_session()
        try:
            since = datetime.utcnow() - timedelta(hours=hours)
            return session.query(CallRecord).filter(
                CallRecord.created_at >= since
            ).order_by(desc(CallRecord.created_at)).all()
        except SQLAlchemyError as e:
            logger.error(f"Failed to get recent calls: {e}")
            return []
        finally:
            session.close()

# Global instance
database_service = DatabaseService()
