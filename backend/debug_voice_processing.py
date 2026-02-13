#!/usr/bin/env python3
import requests
import time

def debug_voice_processing():
    """Debug what happens during voice processing"""
    backend_url = "http://localhost:8000"
    
    print("🔍 Debugging voice processing...")
    
    # Step 1: Check initial state
    print("\n📋 Step 1: Initial API call")
    response = requests.get(f"{backend_url}/api/calls", timeout=5)
    if response.status_code == 200:
        calls = response.json()
        print(f"✅ Initial calls: {len(calls)}")
    else:
        print(f"❌ Initial call failed: {response.text}")
        return
    
    # Step 2: Process one voice call
    print("\n📋 Step 2: Process voice call")
    test_voice_data = {
        'SpeechResult': 'Medical emergency at 123 Main Street, patient having difficulty breathing',
        'CallSid': f'debug_test_{int(time.time())}',
        'From': '+15551234567'
    }
    
    response = requests.post(
        f"{backend_url}/api/voice/process",
        data=test_voice_data,
        timeout=10
    )
    
    if response.status_code == 200:
        print("✅ Voice processing successful")
    else:
        print(f"❌ Voice processing failed: {response.status_code} - {response.text}")
        return
    
    # Step 3: Wait and check database
    time.sleep(2)
    
    # Step 4: Check API again
    print("\n📋 Step 3: API call after voice processing")
    response = requests.get(f"{backend_url}/api/calls", timeout=5)
    if response.status_code == 200:
        calls = response.json()
        print(f"✅ Calls after processing: {len(calls)}")
    else:
        print(f"❌ API call after processing failed: {response.status_code} - {response.text}")
        
        # Let's check what's in the database directly
        print("\n📋 Step 4: Direct database check")
        import sqlite3
        conn = sqlite3.connect('hackaura.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM call_records')
        total_count = cursor.fetchone()[0]
        print(f"📊 Total records in DB: {total_count}")
        
        cursor.execute('SELECT DISTINCT emergency_type FROM call_records')
        emergency_types = cursor.fetchall()
        print(f"🏥 Emergency types in DB: {[et[0] for et in emergency_types]}")
        
        conn.close()

if __name__ == "__main__":
    debug_voice_processing()
