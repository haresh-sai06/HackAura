#!/usr/bin/env python3

"""
Script to fix enum data in the database by converting all values to uppercase
"""

import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models.database import Base, CallRecord, EmergencyType, SeverityLevel, CallStatus, EmergencyService
from utils.enum_utils import normalize_emergency_type, normalize_severity_level, normalize_call_status, normalize_emergency_service
from config import settings

def fix_database_enums():
    """Fix all enum values in the database to be proper uppercase enums"""
    
    # Create database connection
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    session = SessionLocal()
    
    try:
        # Get all records
        calls = session.query(CallRecord).all()
        print(f"Found {len(calls)} records to check")
        
        fixed_count = 0
        for call in calls:
            needs_update = False
            updates = {}
            
            # Check and fix emergency_type
            if call.emergency_type:
                try:
                    normalized_type = normalize_emergency_type(call.emergency_type)
                    if call.emergency_type != normalized_type:
                        updates['emergency_type'] = normalized_type
                        needs_update = True
                except Exception as e:
                    print(f"Error normalizing emergency_type for call {call.id}: {e}")
                    continue
            
            # Check and fix severity_level
            if call.severity_level:
                try:
                    normalized_severity = normalize_severity_level(call.severity_level)
                    if call.severity_level != normalized_severity:
                        updates['severity_level'] = normalized_severity
                        needs_update = True
                except Exception as e:
                    print(f"Error normalizing severity_level for call {call.id}: {e}")
                    continue
            
            # Check and fix status
            if call.status:
                try:
                    normalized_status = normalize_call_status(call.status)
                    if call.status != normalized_status:
                        updates['status'] = normalized_status
                        needs_update = True
                except Exception as e:
                    print(f"Error normalizing status for call {call.id}: {e}")
                    continue
            
            # Check and fix assigned_service
            if call.assigned_service:
                try:
                    normalized_service = normalize_emergency_service(call.assigned_service)
                    if call.assigned_service != normalized_service:
                        updates['assigned_service'] = normalized_service
                        needs_update = True
                except Exception as e:
                    print(f"Error normalizing assigned_service for call {call.id}: {e}")
                    continue
            
            # Apply updates if needed
            if needs_update:
                for field, value in updates.items():
                    setattr(call, field, value)
                
                print(f"Fixed call {call.id}: {updates}")
                fixed_count += 1
        
        # Commit all changes
        if fixed_count > 0:
            session.commit()
            print(f"✅ Fixed {fixed_count} records")
        else:
            print("✅ All records already have correct enum values")
            
    except Exception as e:
        session.rollback()
        print(f"❌ Error fixing database: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    print("🔧 Fixing enum data in database...")
    fix_database_enums()
    print("✅ Database enum fixing complete!")
