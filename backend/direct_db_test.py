#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.database_service import database_service

def test_direct_db():
    """Test direct database access"""
    print("🔍 Testing direct database access...")
    
    try:
        calls = database_service.get_all_calls(limit=10)
        print(f"✅ Direct DB access returned {len(calls)} calls")
        
        if calls:
            print(f"📞 First call: ID={calls[0].id}, Type={calls[0].emergency_type}, Status={calls[0].status}")
        
        return True
    except Exception as e:
        print(f"❌ Direct DB access failed: {e}")
        return False

if __name__ == "__main__":
    test_direct_db()
