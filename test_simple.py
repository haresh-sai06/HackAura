import asyncio
from services.gemini_service import gemini_service

async def test_simple():
    try:
        # Test simple Gemini call
        response = await gemini_service.generate_response("test123", "Hello how are you?")
        print(f"✅ Test successful: {response}")
        return response
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return None

if __name__ == "__main__":
    result = asyncio.run(test_simple())
    print(f"Final result: {result}")
