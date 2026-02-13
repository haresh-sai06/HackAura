"""
RAPID-100 Basic Triage Testing (No API calls required)
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.classification_engine import classification_engine
from services.severity_engine import severity_engine
from services.routing_engine import routing_engine
from services.summary_engine import summary_engine
from models.emergency_schema import EmergencyType, SeverityLevel

async def test_basic_triage():
    """Test individual triage components without API calls"""
    
    test_cases = [
        {
            "name": "Critical Medical Emergency",
            "transcript": "Help! My father is 65 years old and he's not breathing. He collapsed on the floor at MG Road. I think he's having a heart attack. Please send an ambulance immediately.",
            "expected_type": EmergencyType.MEDICAL,
            "expected_severity": SeverityLevel.LEVEL_1
        },
        {
            "name": "Fire Emergency",
            "transcript": "There's a fire spreading in our apartment building on Brigade Road. The smoke is everywhere and people are trapped. Please send the fire department right now.",
            "expected_type": EmergencyType.FIRE,
            "expected_severity": SeverityLevel.LEVEL_1
        },
        {
            "name": "Moderate Medical Issue",
            "transcript": "My son fell and cut his arm. He's bleeding but it's not too bad. He's 10 years old and needs stitches. We're at home in Indiranagar.",
            "expected_type": EmergencyType.MEDICAL,
            "expected_severity": SeverityLevel.LEVEL_3
        }
    ]
    
    print("🚨 RAPID-100 Basic Triage Test Suite")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['name']}")
        print("-" * 40)
        print(f"Input: {test_case['transcript']}")
        
        try:
            # Step 1: Classification
            classification = classification_engine.classify(test_case['transcript'])
            print(f"\n🔍 Classification:")
            print(f"  Emergency Type: {classification.emergency_type.value}")
            print(f"  Confidence: {classification.confidence:.2f}")
            
            # Step 2: Severity Assessment
            severity = severity_engine.calculate(test_case['transcript'])
            print(f"\n⚡ Severity:")
            print(f"  Level: {severity.level.value}")
            print(f"  Score: {severity.score}/100")
            print(f"  Risk Indicators: {', '.join(severity.risk_indicators[:3])}")
            
            # Step 3: Routing
            routing = routing_engine.route(classification.emergency_type, severity.level)
            print(f"\n🚑 Routing:")
            print(f"  Assigned Service: {routing.assigned_service.value}")
            print(f"  Priority: {routing.priority}")
            
            # Step 4: Summary
            summary = summary_engine.generate(
                test_case['transcript'],
                classification.emergency_type,
                severity.level,
                severity.risk_indicators
            )
            print(f"\n📝 Summary:")
            print(f"  {summary}")
            
            # Validation
            type_match = classification.emergency_type == test_case['expected_type']
            severity_match = severity.level == test_case['expected_severity']
            
            print(f"\n✅ Validation:")
            print(f"  Type Match: {'✅' if type_match else '❌'}")
            print(f"  Severity Match: {'✅' if severity_match else '❌'}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("🏁 Basic Test Suite Complete")

if __name__ == "__main__":
    asyncio.run(test_basic_triage())
