"""
Ultra-Fast Response Generator
Provides instant safety precautions and guidance for emergency types
"""

import logging
import time
from typing import Dict, List
from services.production_ultra_fast_service import production_ultra_fast_service

logger = logging.getLogger(__name__)


class UltraFastResponseGenerator:
    """Generate instant safety responses for ultra-fast triage"""
    
    def __init__(self):
        self.safety_responses = {
            'Fire': {
                'immediate_actions': [
                    'Evacuate the area immediately',
                    'Do not use elevators',
                    'Call emergency services',
                    'Close doors behind you'
                ],
                'safety_precautions': [
                    'Stay low to avoid smoke inhalation',
                    'Feel doors before opening - hot means fire is near',
                    'Use stairs only for evacuation',
                    'Meet at designated assembly point'
                ],
                'what_to_say': 'There is a fire. Evacuate immediately and call 911. Do not use elevators.',
                'priority_level': 'CRITICAL'
            },
            'Medical': {
                'immediate_actions': [
                    'Call emergency services immediately',
                    'Check breathing and pulse',
                    'Keep person comfortable',
                    'Clear airway if needed'
                ],
                'safety_precautions': [
                    'Do not move person unless in danger',
                    'Apply direct pressure to bleeding',
                    'Keep person warm',
                    'Monitor consciousness'
                ],
                'what_to_say': 'Medical emergency detected. Call 911 immediately. Check if person is breathing.',
                'priority_level': 'CRITICAL'
            },
            'Crime': {
                'immediate_actions': [
                    'Move to safe location immediately',
                    'Lock doors and windows',
                    'Call police from safe location',
                    'Do not confront suspect'
                ],
                'safety_precautions': [
                    'Stay away from windows',
                    'Silence your phone',
                    'Have escape route planned',
                    'Do not open door to strangers'
                ],
                'what_to_say': 'Dangerous situation. Move to safe location and call police. Lock doors.',
                'priority_level': 'HIGH'
            },
            'Accident': {
                'immediate_actions': [
                    'Move to safe location away from traffic',
                    'Turn on hazard lights immediately',
                    'Check for injuries and provide first aid',
                    'Call emergency services if serious injuries',
                    'Take photos of scene if safe to do so'
                ],
                'safety_precautions': [
                    'Stay away from moving traffic and warn other drivers',
                    'Set up warning triangles or flares behind your vehicle',
                    'Do not move injured persons unless there is immediate danger',
                    'Apply direct pressure to bleeding wounds',
                    'Keep injured persons warm with blankets or clothing',
                    'Exchange information with other drivers involved',
                    'Document scene with photos when safe',
                    'Follow emergency dispatcher instructions exactly'
                ],
                'what_to_say': 'Help is coming! Emergency services are being dispatched now. Move to safe location away from traffic and turn on hazard lights immediately. Check for injuries and provide first aid. Call emergency services if serious injuries. Take photos of scene if safe to do so. Stay away from moving traffic and set up warning triangles or flares behind your vehicle. Do not move injured persons unless there is immediate danger. Apply direct pressure to bleeding wounds and keep injured persons warm with blankets or clothing. Exchange information with other drivers involved and document scene with photos when safe. Follow emergency dispatcher instructions exactly.',
                'priority_level': 'HIGH'
            },
            'Other': {
                'immediate_actions': [
                    'Assess the situation',
                    'Call emergency services if needed',
                    'Keep calm',
                    'Follow dispatcher instructions'
                ],
                'safety_precautions': [
                    'Stay aware of surroundings',
                    'Have phone available',
                    'Know emergency numbers',
                    'Keep first aid kit accessible'
                ],
                'what_to_say': 'Emergency situation detected. Stay calm and call for help if needed.',
                'priority_level': 'MODERATE'
            }
        }
        
        logger.info("🗣️ Ultra-Fast Response Generator initialized")
    
    async def process_with_response(self, transcript: str) -> Dict:
        """
        Process emergency and return triage + safety response
        
        Args:
            transcript: Emergency call transcript
            
        Returns:
            Complete response with triage and safety guidance
        """
        start_time = time.time()
        
        # Get ultra-fast triage result
        triage_result = await production_ultra_fast_service.process(transcript)
        
        # Generate safety response based on category
        safety_response = self._generate_safety_response(triage_result['category'])
        
        processing_time = (time.time() - start_time) * 1000
        
        return {
            # Triage information
            'category': triage_result['category'],
            'priority': triage_result['priority'],
            'reasoning_byte': triage_result['reasoning_byte'],
            'processing_time_ms': processing_time,
            
            # Safety response
            'what_to_say': safety_response['what_to_say'],
            'immediate_actions': safety_response['immediate_actions'],
            'safety_precautions': safety_response['safety_precautions'],
            'priority_level': safety_response['priority_level'],
            
            # Metadata
            'response_type': 'triage_plus_safety',
            'confidence': 0.85  # High confidence for rule-based
        }
    
    def _generate_safety_response(self, category: str) -> Dict:
        """Generate safety response based on emergency category"""
        return self.safety_responses.get(category, self.safety_responses['Other'])
    
    def get_voice_response(self, category: str) -> str:
        """Get voice-friendly response for emergency"""
        response = self._generate_safety_response(category)
        return response['what_to_say']
    
    def get_sms_response(self, category: str) -> str:
        """Get SMS-friendly response"""
        response = self._generate_safety_response(category)
        
        actions = '\n'.join([f'• {action}' for action in response['immediate_actions'][:3]])
        precautions = '\n'.join([f'• {prec}' for prec in response['safety_precautions'][:2]])
        
        return f"""{response['what_to_say']}

IMMEDIATE ACTIONS:
{actions}

SAFETY PRECAUTIONS:
{precautions}

Priority: {response['priority_level']}"""
    
    def get_dispatcher_summary(self, category: str, priority: int, location: str = None) -> str:
        """Get summary for emergency dispatcher"""
        response = self._generate_safety_response(category)
        
        summary = f"EMERGENCY: {category.upper()} - Priority {priority}"
        summary += f"\n{response['what_to_say']}"
        
        if location:
            summary += f"\nLocation: {location}"
        
        summary += f"\nRecommended Actions: {', '.join(response['immediate_actions'][:2])}"
        
        return summary


# Create singleton instance
ultra_fast_response_generator = UltraFastResponseGenerator()
