import logging
import sys

# Configure logging to see the actual error
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from services.database_service import database_service
    print("✅ Database service imported successfully")
    
    # Test getting calls
    calls = database_service.get_all_calls(limit=10)
    print(f"✅ Retrieved {len(calls)} calls from database")
    
    for call in calls:
        print(f"Call: {call.id} - {call.emergency_type} - {call.status}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
