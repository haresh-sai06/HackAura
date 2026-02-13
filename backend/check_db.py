#!/usr/bin/env python3
import sqlite3
import json

def check_database():
    # Connect to the correct database
    conn = sqlite3.connect('hackaura.db')
    cursor = conn.cursor()

    # Check if calls table exists and get its structure
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='call_records'")
    table_exists = cursor.fetchone()

    if table_exists:
        print('✅ call_records table exists')
        
        # Get table structure
        cursor.execute('PRAGMA table_info(call_records)')
        columns = cursor.fetchall()
        print(f'📊 Table has {len(columns)} columns')
        
        # Get total count
        cursor.execute('SELECT COUNT(*) FROM call_records')
        total_count = cursor.fetchone()[0]
        print(f'📞 Total records in database: {total_count}')
        
        if total_count > 0:
            # Get sample records with raw data
            cursor.execute('SELECT id, call_sid, from_number, emergency_type, severity_level, status, created_at FROM call_records ORDER BY created_at DESC LIMIT 3')
            recent_calls = cursor.fetchall()
            print(f'📋 Recent calls (raw data):')
            for call in recent_calls:
                print(f'   ID: {call[0]}, SID: {call[1]}, Type: {repr(call[3])}, Severity: {repr(call[4])}, Status: {repr(call[5])}, Created: {call[6]}')
            
            # Check what emergency_types are actually stored
            cursor.execute('SELECT DISTINCT emergency_type FROM call_records')
            emergency_types = cursor.fetchall()
            print(f'🏥 Emergency types in DB: {[et[0] for et in emergency_types]}')
            
            # Check what severity_levels are actually stored
            cursor.execute('SELECT DISTINCT severity_level FROM call_records')
            severity_levels = cursor.fetchall()
            print(f'🚨 Severity levels in DB: {[sl[0] for sl in severity_levels]}')
            
            # Check what statuses are actually stored
            cursor.execute('SELECT DISTINCT status FROM call_records')
            statuses = cursor.fetchall()
            print(f'📊 Statuses in DB: {[s[0] for s in statuses]}')
            
            # Check what assigned_services are actually stored
            cursor.execute('SELECT DISTINCT assigned_service FROM call_records')
            services = cursor.fetchall()
            print(f'🚑 Assigned services in DB: {[s[0] for s in services]}')
        else:
            print('⚠️ No records found in database')
    else:
        print('❌ call_records table does not exist')

    conn.close()

if __name__ == "__main__":
    check_database()
