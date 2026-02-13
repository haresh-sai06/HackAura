#!/usr/bin/env python3

import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('hackaura.db')
cursor = conn.cursor()

# Check what's in the call_records table
try:
    cursor.execute("SELECT id, call_sid, emergency_type, severity_level, status FROM call_records LIMIT 5")
    records = cursor.fetchall()
    
    print(f"Found {len(records)} records:")
    for record in records:
        print(f"ID: {record[0]}, SID: {record[1]}, Type: {record[2]}, Severity: {record[3]}, Status: {record[4]}")
        
    # Check total count
    cursor.execute("SELECT COUNT(*) FROM call_records")
    total_count = cursor.fetchone()[0]
    print(f"\nTotal records in database: {total_count}")
    
    # Show unique emergency types
    cursor.execute("SELECT DISTINCT emergency_type FROM call_records")
    types = [row[0] for row in cursor.fetchall()]
    print(f"Emergency types in DB: {types}")
    
    # Show unique statuses
    cursor.execute("SELECT DISTINCT status FROM call_records")
    statuses = [row[0] for row in cursor.fetchall()]
    print(f"Statuses in DB: {statuses}")
    
except Exception as e:
    print(f"Error: {e}")

conn.close()
