#!/usr/bin/env python3
import sqlite3

def fix_database():
    """Fix enum values in database to match model definitions"""
    conn = sqlite3.connect('hackaura.db')
    cursor = conn.cursor()
    
    print("🔧 Fixing database enum values...")
    
    # Fix emergency_type values - normalize to uppercase
    cursor.execute("UPDATE call_records SET emergency_type = 'MEDICAL' WHERE emergency_type = 'medical'")
    cursor.execute("UPDATE call_records SET emergency_type = 'FIRE' WHERE emergency_type = 'fire'")
    cursor.execute("UPDATE call_records SET emergency_type = 'POLICE' WHERE emergency_type = 'police'")
    cursor.execute("UPDATE call_records SET emergency_type = 'ACCIDENT' WHERE emergency_type = 'accident'")
    cursor.execute("UPDATE call_records SET emergency_type = 'MENTAL_HEALTH' WHERE emergency_type = 'mental_health'")
    cursor.execute("UPDATE call_records SET emergency_type = 'NATURAL_DISASTER' WHERE emergency_type = 'natural_disaster'")
    cursor.execute("UPDATE call_records SET emergency_type = 'OTHER' WHERE emergency_type = 'other'")
    
    # Fix severity_level values - normalize to uppercase
    cursor.execute("UPDATE call_records SET severity_level = 'LEVEL_1' WHERE severity_level = 'Level 1'")
    cursor.execute("UPDATE call_records SET severity_level = 'LEVEL_2' WHERE severity_level = 'Level 2'")
    cursor.execute("UPDATE call_records SET severity_level = 'LEVEL_3' WHERE severity_level = 'Level 3'")
    cursor.execute("UPDATE call_records SET severity_level = 'LEVEL_4' WHERE severity_level = 'Level 4'")
    
    # Fix status values - normalize to uppercase
    cursor.execute("UPDATE call_records SET status = 'PENDING' WHERE status = 'pending'")
    cursor.execute("UPDATE call_records SET status = 'IN_PROGRESS' WHERE status = 'in_progress'")
    cursor.execute("UPDATE call_records SET status = 'DISPATCHED' WHERE status = 'dispatched'")
    cursor.execute("UPDATE call_records SET status = 'RESOLVED' WHERE status = 'resolved'")
    cursor.execute("UPDATE call_records SET status = 'CANCELLED' WHERE status = 'cancelled'")
    
    # Fix assigned_service values - normalize to uppercase
    cursor.execute("UPDATE call_records SET assigned_service = 'AMBULANCE' WHERE assigned_service IN ('Ambulance', 'ambulance')")
    cursor.execute("UPDATE call_records SET assigned_service = 'FIRE_DEPARTMENT' WHERE assigned_service IN ('Fire Department', 'fire_department')")
    cursor.execute("UPDATE call_records SET assigned_service = 'POLICE' WHERE assigned_service IN ('Police', 'police')")
    cursor.execute("UPDATE call_records SET assigned_service = 'MULTIPLE_SERVICES' WHERE assigned_service IN ('Multiple Services', 'multiple_services')")
    
    # Check the changes
    cursor.execute('SELECT DISTINCT emergency_type FROM call_records')
    emergency_types = cursor.fetchall()
    print(f'🏥 Fixed emergency types: {[et[0] for et in emergency_types]}')
    
    cursor.execute('SELECT DISTINCT severity_level FROM call_records')
    severity_levels = cursor.fetchall()
    print(f'🚨 Fixed severity levels: {[sl[0] for sl in severity_levels]}')
    
    cursor.execute('SELECT DISTINCT status FROM call_records')
    statuses = cursor.fetchall()
    print(f'📊 Fixed statuses: {[s[0] for s in statuses]}')
    
    cursor.execute('SELECT DISTINCT assigned_service FROM call_records')
    services = cursor.fetchall()
    print(f'🚑 Fixed assigned services: {[s[0] for s in services]}')
    
    conn.commit()
    conn.close()
    print("✅ Database fixed successfully!")

if __name__ == "__main__":
    fix_database()
