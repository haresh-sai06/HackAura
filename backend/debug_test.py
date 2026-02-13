#!/usr/bin/env python3
import requests

def debug_api_calls():
    """Debug the API calls to understand the discrepancy"""
    backend_url = "http://localhost:8000"
    
    print("🔍 Debugging API calls...")
    
    # Test 1: Direct API call (like in Test 2)
    print("\n📋 Test 1: Direct API call")
    response = requests.get(f"{backend_url}/api/calls", timeout=5)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        calls = response.json()
        print(f"✅ Direct call returned {len(calls)} calls")
    else:
        print(f"❌ Direct call failed: {response.text}")
    
    # Test 2: Same call as in Test 4
    print("\n📋 Test 2: Test 4 style call")
    initial_response = requests.get(f"{backend_url}/api/calls", timeout=5)
    print(f"Status Code: {initial_response.status_code}")
    if initial_response.status_code == 200:
        initial_calls = initial_response.json()
        initial_count = len(initial_calls)
        print(f"✅ Test 4 style call returned {initial_count} calls")
    else:
        print(f"❌ Test 4 style call failed: {initial_response.text}")
        initial_calls = []
        initial_count = 0
    
    print(f"\n📊 Comparison:")
    print(f"   Direct call: {len(calls) if response.status_code == 200 else 'Failed'}")
    print(f"   Test 4 style: {initial_count}")

if __name__ == "__main__":
    debug_api_calls()
