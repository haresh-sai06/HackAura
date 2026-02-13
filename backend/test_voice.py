#!/usr/bin/env python3
"""
Test script to simulate voice-to-text emergency processing
"""
import requests
import json

def test_voice_processing():
    """Test the voice processing endpoint with sample emergency inputs"""
    
    base_url = "http://localhost:8000"
    
    # Test cases with different emergency scenarios
    test_cases = [
        "There's a fire in my kitchen and the smoke is spreading fast",
        "My chest hurts and I can't breathe properly",
        "Car accident on MG Road, two people injured",
        "Someone is breaking into my house right now",
        "I fell down the stairs and my leg is broken"
    ]
    
    print("🚑 Testing Voice-to-Text Emergency Processing")
    print("=" * 50)
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_input}")
        print("-" * 40)
        
        # Simulate form data that Twilio would send
        form_data = {
            'SpeechResult': test_input,
            'CallSid': f'test_call_{i}',
            'From': '+1234567890'
        }
        
        try:
            # Send POST request to voice processing endpoint
            response = requests.post(
                f"{base_url}/api/voice/process",
                data=form_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            if response.status_code == 200:
                print("✅ Request successful")
                print(f"📊 Response Status: {response.status_code}")
                print(f"📄 Response Type: {response.headers.get('content-type', 'unknown')}")
                
                # The response should be TwiML (XML)
                if 'xml' in response.headers.get('content-type', '').lower():
                    print("📞 TwiML response generated successfully")
                    # Show a snippet of the TwiML response
                    response_preview = response.text[:200] + "..." if len(response.text) > 200 else response.text
                    print(f"📋 Response Preview: {response_preview}")
                else:
                    print(f"📋 Response: {response.text}")
                    
            else:
                print(f"❌ Request failed with status {response.status_code}")
                print(f"📋 Error Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection error - make sure the server is running on localhost:8000")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed")

if __name__ == "__main__":
    test_voice_processing()
