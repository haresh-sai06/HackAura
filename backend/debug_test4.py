#!/usr/bin/env python3
import requests
import json

def debug_test4():
    """Debug the exact issue with Test 4"""
    backend_url = "http://localhost:8000"
    
    print("🔍 Debugging Test 4 issue...")
    
    # Replicate EXACTLY what Test 2 does
    print("\n📋 Test 2 replication:")
    response = requests.get(f"{backend_url}/api/calls", timeout=5)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        calls = response.json()
        print(f"✅ Test 2 style returned {len(calls)} calls")
    else:
        print(f"❌ Test 2 style failed: {response.text}")
    
    # Replicate EXACTLY what Test 4 does
    print("\n📋 Test 4 replication:")
    initial_response = requests.get(f"{backend_url}/api/calls", timeout=5)
    print(f"Status Code: {initial_response.status_code}")
    
    initial_calls = []
    if initial_response.status_code == 200:
        try:
            initial_calls = initial_response.json()
            print(f"✅ JSON parsing successful, got {len(initial_calls)} calls")
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print(f"Response text: {initial_response.text[:200]}...")
    else:
        print(f"❌ Request failed: {initial_response.text}")
    
    initial_count = len(initial_calls)
    print(f"📊 Initial call count: {initial_count}")
    
    # Let's also check the response headers
    print(f"\n📋 Response headers:")
    for key, value in initial_response.headers.items():
        print(f"   {key}: {value}")

if __name__ == "__main__":
    debug_test4()
