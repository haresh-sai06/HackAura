"""
RAPID-100 Ollama Integration Test Script
Tests the new Ollama-based triage engine against various emergency scenarios
"""

import asyncio
import json
import time
from services.ollama_triage_service import ollama_triage_service
from models.emergency_schema import EmergencyType, SeverityLevel, EmergencyService

# Test scenarios covering all emergency types
TEST_SCENARIOS = [
    {
        "name": "Medical Emergency - Heart Attack",
        "transcript": "My husband is having severe chest pain and difficulty breathing. He collapsed on the floor. Please hurry!"
    },
    {
        "name": "Fire Emergency",
        "transcript": "There's a massive fire in the apartment building! The building is on fire with flames spreading. We need the fire department NOW!"
    },
    {
        "name": "Police - Violent Crime",
        "transcript": "There's someone breaking into my house! I can hear them trying to force the door open. They have a weapon. Please send police immediately!"
    },
    {
        "name": "Traffic Accident",
        "transcript": "We just had a major car collision on the highway. Multiple vehicles are involved. Some people are trapped in their cars."
    },
    {
        "name": "Mental Health Crisis",
        "transcript": "My friend is having a severe panic attack and talking about suicide. They're overwhelmed and won't calm down. This is a mental health crisis."
    },
    {
        "name": "Moderate Medical Issue",
        "transcript": "I fell and twisted my ankle pretty badly. I can't walk on it. It's swelling but no major bleeding."
    },
    {
        "name": "Non-emergency",
        "transcript": "I have a small cut on my finger from cooking. Just wondering if I should get it checked."
    }
]


async def test_ollama_triage():
    """Run comprehensive tests of the Ollama triage system"""
    
    print("=" * 80)
    print("🤖 RAPID-100 Ollama Triage System - Integration Test")
    print("=" * 80)
    print()
    
    results = []
    
    for i, scenario in enumerate(TEST_SCENARIOS, 1):
        print(f"\n📋 Test {i}/{len(TEST_SCENARIOS)}: {scenario['name']}")
        print("-" * 80)
        print(f"Transcript: {scenario['transcript'][:100]}...")
        print()
        
        try:
            # Process with Ollama
            start_time = time.time()
            result = await ollama_triage_service.process(scenario['transcript'])
            elapsed = time.time() - start_time
            
            # Display results
            print(f"✅ Classification Results:")
            print(f"   🚨 Emergency Type: {result.emergency_type.value}")
            print(f"   🔴 Severity Level: {result.severity_level.value}")
            print(f"   📊 Severity Score: {result.severity_score}/100")
            print(f"   🏥 Assigned Service: {result.assigned_service.value}")
            print(f"   ⚡ Priority: {result.priority}/10")
            print(f"   🎯 Confidence: {result.confidence:.1%}")
            print(f"   ⏱️  Processing Time: {elapsed*1000:.2f}ms")
            print(f"   📝 Summary: {result.summary}")
            if result.risk_indicators:
                print(f"   ⚠️  Risk Factors: {', '.join(result.risk_indicators)}")
            if result.location:
                print(f"   📍 Location: {result.location}")
            
            results.append({
                "scenario": scenario['name'],
                "success": True,
                "emergency_type": result.emergency_type.value,
                "severity": result.severity_level.value,
                "processing_time_ms": elapsed * 1000
            })
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results.append({
                "scenario": scenario['name'],
                "success": False,
                "error": str(e)
            })
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("📊 Test Summary")
    print("=" * 80)
    
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    print(f"\n✅ Successful: {successful}/{len(results)}")
    print(f"❌ Failed: {failed}/{len(results)}")
    
    if successful > 0:
        processing_times = [r['processing_time_ms'] for r in results if r['success']]
        avg_time = sum(processing_times) / len(processing_times)
        min_time = min(processing_times)
        max_time = max(processing_times)
        
        print(f"\n⏱️  Processing Performance:")
        print(f"   Average: {avg_time:.2f}ms")
        print(f"   Minimum: {min_time:.2f}ms")
        print(f"   Maximum: {max_time:.2f}ms")
    
    # Service statistics
    stats = ollama_triage_service.get_stats()
    print(f"\n🤖 Ollama Service Statistics:")
    print(f"   Total Calls: {stats['total_calls']}")
    print(f"   Average Latency: {stats['avg_ms']:.2f}ms")
    
    print("\n" + "=" * 80)
    print("✅ Integration Test Complete!")
    print("=" * 80)
    
    return results


async def quick_test():
    """Quick test of a single scenario"""
    print("\n🚀 Quick Test - Fire Emergency")
    result = await ollama_triage_service.process(
        "There's a massive fire in the apartment building!"
    )
    print(f"Type: {result.emergency_type.value}")
    print(f"Severity: {result.severity_level.value}")
    print(f"Service: {result.assigned_service.value}")
    print(f"Summary: {result.summary}")
    print(f"Processing Time: {result.processing_time_ms:.2f}ms")


if __name__ == "__main__":
    print("\n🎯 Starting RAPID-100 Ollama Integration Tests\n")
    
    # Run comprehensive tests
    results = asyncio.run(test_ollama_triage())
    
    # Save results to file
    with open('ollama_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\n📁 Results saved to: ollama_test_results.json")
