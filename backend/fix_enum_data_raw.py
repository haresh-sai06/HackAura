#!/usr/bin/env python3

"""
Script to fix enum data in the database using raw SQL
"""

import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import settings

def fix_database_enums_raw():
    """Fix all enum values in the database using raw SQL"""
    
    # Create database connection
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,  # Disable echo for cleaner output
        connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
    )
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        print("🔧 Fixing enum data using raw SQL...")
        
        # Fix emergency_type
        result = session.execute(text("""
            UPDATE call_records 
            SET emergency_type = UPPER(emergency_type)
            WHERE emergency_type != UPPER(emergency_type)
        """))
        emergency_fixed = result.rowcount
        
        # Fix severity_level
        result = session.execute(text("""
            UPDATE call_records 
            SET severity_level = UPPER(severity_level)
            WHERE severity_level != UPPER(severity_level)
        """))
        severity_fixed = result.rowcount
        
        # Fix status
        result = session.execute(text("""
            UPDATE call_records 
            SET status = UPPER(status)
            WHERE status != UPPER(status)
        """))
        status_fixed = result.rowcount
        
        # Fix assigned_service
        result = session.execute(text("""
            UPDATE call_records 
            SET assigned_service = UPPER(assigned_service)
            WHERE assigned_service != UPPER(assigned_service)
        """))
        service_fixed = result.rowcount
        
        # Fix common variations
        # Replace underscores with spaces in emergency_type
        result = session.execute(text("""
            UPDATE call_records 
            SET emergency_type = REPLACE(emergency_type, '_', '')
            WHERE emergency_type LIKE '%_%'
        """))
        underscore_fixed = result.rowcount
        
        session.commit()
        
        print(f"✅ Fixed enum values:")
        print(f"   Emergency types: {emergency_fixed}")
        print(f"   Severity levels: {severity_fixed}")
        print(f"   Statuses: {status_fixed}")
        print(f"   Assigned services: {service_fixed}")
        print(f"   Underscore removal: {underscore_fixed}")
        
        # Show sample of fixed data
        result = session.execute(text("""
            SELECT id, emergency_type, severity_level, status, assigned_service
            FROM call_records 
            LIMIT 5
        """))
        sample_data = result.fetchall()
        
        print("\n📊 Sample fixed data:")
        for row in sample_data:
            print(f"   ID: {row[0]}, Type: {row[1]}, Severity: {row[2]}, Status: {row[3]}, Service: {row[4]}")
            
    except Exception as e:
        session.rollback()
        print(f"❌ Error fixing database: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    fix_database_enums_raw()
    print("✅ Database enum fixing complete!")
