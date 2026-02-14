"""
Hybrid Emergency Triage Service
Combines instant rule-based classification with AI safety responses
"""

import logging
import time
from typing import Dict, List
from services.database_service import database_service
from models.database import EmergencyType, SeverityLevel, EmergencyService, CallRecord

logger = logging.getLogger(__name__)


class HybridTriageService:
    """Hybrid service: Instant classification + AI safety responses"""
    
    def __init__(self):
        # Rule-based keyword classification for instant response
        self.emergency_keywords = {
            'Fire': {
                'keywords': ['fire', 'burning', 'smoke', 'flames', 'explosion', 'caught fire', 'massive fire'],
                'high_severity': ['massive', 'building', 'trap', 'can breathe', 'explosion'],
                'service': EmergencyService.FIRE_DEPARTMENT,
                'category': EmergencyType.FIRE
            },
            'Medical': {
                'keywords': ['heart attack', 'stroke', 'bleeding', 'unconscious', 'chest pain', 'difficulty breathing', 'having trouble breathing'],
                'high_severity': ['can breathe', 'unconscious', 'bleeding heavily', 'heart attack'],
                'service': EmergencyService.AMBULANCE,
                'category': EmergencyType.MEDICAL
            },
            'Police': {
                'keywords': ['shooting', 'gun', 'robbery', 'assault', 'break in', 'intruder', 'violence', 'active shooter'],
                'high_severity': ['gun', 'shooting', 'weapon', 'happening now'],
                'service': EmergencyService.POLICE,
                'category': EmergencyType.POLICE
            },
            'Accident': {
                'keywords': ['car crash', 'accident', 'collision', 'hit and run', 'traffic', 'highway', 'pileup'],
                'high_severity': ['multiple cars', 'truck', 'highway', 'serious injury'],
                'service': EmergencyService.MULTIPLE_SERVICES,
                'category': EmergencyType.ACCIDENT
            },
            'Mental_Health': {
                'keywords': ['suicide', 'depression', 'anxiety', 'panic attack', 'mental health', 'harm myself'],
                'high_severity': ['suicide', 'harm myself', 'can cope'],
                'service': EmergencyService.CRISIS_RESPONSE,
                'category': EmergencyType.MENTAL_HEALTH
            }
        }
        
        # Conversation state management
        self.active_conversations = {}  # Track ongoing conversations
        
        # Safety responses for each category
        self.safety_responses = {
            'Fire': {
                'what_to_say': 'Help is coming! Fire department is being dispatched now. Evacuate immediately and do not use elevators. Stay low to avoid smoke inhalation and feel doors before opening. Use stairs only for evacuation and help others evacuate if safe to do so.',
                'immediate_actions': [
                    'Evacuate the area immediately',
                    'Do not use elevators',
                    'Close doors behind you',
                    'Move to designated assembly point'
                ],
                'dispatched_service': 'Fire Department',
                'danger_question': 'Is the fire spreading or are people trapped?',
                'escalated_response': 'Help is on the way! Priority increased to critical. Stay on the line and we will end the call when help arrives.'
            },
            'Medical': {
                'what_to_say': 'Help is coming! Ambulance is being dispatched now. Check if person is breathing and stay on the line. Keep person comfortable and apply direct pressure to bleeding. Monitor consciousness and have medical history ready.',
                'immediate_actions': [
                    'Check breathing and pulse',
                    'Keep person comfortable',
                    'Clear airway if needed',
                    'Apply direct pressure to bleeding'
                ],
                'safety_precautions': [
                    'Do not move person unless in danger',
                    'Keep person warm',
                    'Monitor consciousness',
                    'Have medical history ready'
                ],
                'dispatched_service': 'Ambulance',
                'danger_question': 'Is the person unconscious or not breathing?',
                'escalated_response': 'Help is on the way! Priority increased to critical. Stay on the line and we will end the call when help arrives.'
            },
            'Police': {
                'what_to_say': 'Help is coming! Police are being dispatched now. Move to safe location and lock doors immediately. Stay away from windows and silence your phone. Do not confront suspect and have escape route planned. Follow dispatcher instructions.',
                'immediate_actions': [
                    'Move to safe location immediately',
                    'Lock doors and windows',
                    'Stay away from windows',
                    'Silence your phone'
                ],
                'safety_precautions': [
                    'Do not confront suspect',
                    'Have escape route planned',
                    'Stay quiet and hidden',
                    'Follow dispatcher instructions'
                ],
                'dispatched_service': 'Police',
                'danger_question': 'Is the suspect still present or armed?',
                'escalated_response': 'Help is on the way! Priority increased to critical. Stay on the line and we will end the call when help arrives.'
            },
            'Accident': {
                'what_to_say': 'Help is coming! Emergency services are being dispatched now. Move to safe location away from traffic and turn on hazard lights immediately. Check for injuries and provide first aid. Call emergency services if serious injuries. Take photos of scene if safe to do so. Stay away from moving traffic and set up warning triangles or flares behind your vehicle. Do not move injured persons unless there is immediate danger. Apply direct pressure to bleeding wounds and keep injured persons warm with blankets or clothing. Exchange information with other drivers involved and document scene with photos when safe. Follow emergency dispatcher instructions exactly.',
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
                'dispatched_service': 'Emergency Services',
                'danger_question': 'Are there serious injuries or people trapped?',
                'escalated_response': 'Help is on the way! Priority increased to critical. Multiple services responding. Stay on the line and follow instructions.',
                'post_accident_actions': [
                    'Exchange insurance and contact information',
                    'Document damage with photos and notes',
                    'Seek medical attention even for minor injuries',
                    'Report accident to authorities if not already done',
                    'Preserve evidence and scene integrity'
                ],
                'post_accident_precautions': [
                    'Monitor for delayed injury symptoms',
                    'Keep copies of medical records and bills',
                    'Follow up with insurance claims promptly',
                    'Consider legal consultation if fault is disputed',
                    'Take photos of all damage and injuries'
                ]
            },
            'Mental_Health': {
                'what_to_say': 'Help is coming! Crisis response team is being dispatched now. Stay on the line with us. Move to safe, calm location and remove any potentially harmful items if safe to do so. Breathe slowly and steadily. Keep company with trusted person if possible and remove access to harmful items. Stay in a safe environment and follow crisis counselor guidance.',
                'immediate_actions': [
                    'Stay on the line',
                    'Move to safe, calm location',
                    'Remove any potentially harmful items if safe to do so',
                    'Breathe slowly and steadily'
                ],
                'safety_precautions': [
                    'Keep company with trusted person if possible',
                    'Remove access to harmful items',
                    'Stay in a safe environment',
                    'Follow crisis counselor guidance'
                ],
                'dispatched_service': 'Crisis Response Team',
                'danger_question': 'Is there immediate risk of harm?',
                'escalated_response': 'Help is on the way! Priority increased to critical. Stay on the line and we will end the call when help arrives.'
            },
            'Other': {
                'what_to_say': 'Help is coming! Emergency services are being dispatched now. Stay calm and follow instructions. Keep your mobile phone nearby and have emergency numbers ready. Know your location and stay aware of surroundings.',
                'immediate_actions': [
                    'Stay calm',
                    'Follow dispatcher instructions',
                    'Keep phone available',
                    'Provide clear information'
                ],
                'safety_precautions': [
                    'Stay aware of surroundings',
                    'Have emergency numbers ready',
                    'Keep first aid kit accessible',
                    'Know your location'
                ],
                'dispatched_service': 'Emergency Services',
                'danger_question': 'Is the situation life-threatening?',
                'escalated_response': 'Help is on the way! Priority increased to critical. Stay on the line and we will end the call when help arrives.'
            }
        }
        
        logger.info("🚀 Hybrid Triage Service initialized")
        logger.info("   Strategy: Instant classification + AI safety responses")
    
    def _map_to_frontend_category(self, emergency_type) -> str:
        """Map emergency type enum to frontend category"""
        mapping = {
            EmergencyType.MEDICAL: 'Medical',
            EmergencyType.FIRE: 'Fire',
            EmergencyType.POLICE: 'Crime',
            EmergencyType.ACCIDENT: 'Other',  # Frontend doesn't have Accident category
            EmergencyType.MENTAL_HEALTH: 'Other',
            EmergencyType.NATURAL_DISASTER: 'Other',
            EmergencyType.OTHER: 'Other'
        }
        return mapping.get(emergency_type, 'Other')
    
    def _map_severity_to_level(self, priority: int) -> str:
        """Map priority to severity level for database"""
        if priority == 1:
            return 'LEVEL_1'
        elif priority == 2:
            return 'LEVEL_2'
        elif priority == 3:
            return 'LEVEL_3'
        elif priority == 4:
            return 'LEVEL_4'
        else:
            return 'LEVEL_3'
    
    async def process(self, transcript: str, call_sid: str = None, is_followup: bool = False) -> Dict:
        """
        Process emergency with conversation flow
        
        Args:
            transcript: Emergency call transcript
            call_sid: Call session ID for conversation tracking
            is_followup: Whether this is a follow-up response
            
        Returns:
            Complete emergency response with safety guidance
        """
        start_time = time.time()
        
        try:
            logger.info(f"⚡ Hybrid processing started for: {transcript[:50]}...")
            
            # Check if this is a follow-up response to danger question
            if is_followup and call_sid in self.active_conversations:
                conversation = self.active_conversations[call_sid]
                
                # Check for YES/NO response to danger question
                transcript_lower = transcript.lower()
                if 'yes' in transcript_lower or 'true' in transcript_lower or 'correct' in transcript_lower:
                    # Escalate severity
                    conversation['priority'] = 1
                    conversation['severity'] = 'CRITICAL'
                    conversation['what_to_say'] = conversation['escalated_response']
                    conversation['status'] = 'ESCALATED'
                    
                    logger.info(f"🔥 Severity escalated to CRITICAL for {call_sid}")
                    
                elif 'no' in transcript_lower or 'false' in transcript_lower or 'fine' in transcript_lower:
                    # Keep current severity, end conversation
                    conversation['what_to_say'] = 'Understood. Help is on the way. We will end the call now. Stay safe.'
                    conversation['status'] = 'COMPLETED'
                    
                    logger.info(f"✅ Conversation completed for {call_sid}")
                    
                else:
                    # Unclear response, ask again
                    conversation['what_to_say'] = conversation['danger_question']
                    
                    logger.info(f"❓ Unclear response, asking again for {call_sid}")
                
                # Update conversation state
                self.active_conversations[call_sid] = conversation
                
                # Store and broadcast update
                self._store_conversation_async(conversation, transcript)
                
                processing_time = (time.time() - start_time) * 1000
                conversation['processing_time_ms'] = processing_time
                
                return conversation
            
            # Initial call processing
            # Step 1: Instant rule-based classification
            classification = self._classify_instant(transcript)
            
            # Step 2: Get safety responses
            safety = self.safety_responses.get(classification['category'], self.safety_responses['Other'])
            
            # Step 3: Build complete response with proper timestamps
            processing_time = (time.time() - start_time) * 1000
            current_time = time.time()
            
            # Map category for frontend compatibility
            frontend_category = self._map_to_frontend_category(classification['category'])
            
            result = {
                # Classification results
                'category': frontend_category,
                'priority': classification['priority'],
                'reasoning_byte': classification['reasoning'],
                'processing_time_ms': processing_time,
                'confidence': 0.95,  # High confidence for rule-based
                
                # Safety responses
                'what_to_say': safety['what_to_say'],
                'immediate_actions': safety['immediate_actions'],
                'safety_precautions': safety['safety_precautions'],
                'priority_level': classification['severity'],
                'response_type': 'hybrid_conversation',
                
                # Dispatch information
                'dispatched_service': safety['dispatched_service'],
                'assigned_service': classification['service'].value,
                
                # Conversation state
                'danger_question': safety['danger_question'],
                'escalated_response': safety['escalated_response'],
                'status': 'AWAITING_FOLLOWUP',
                
                # Proper timestamps
                'timestamp': current_time,
                'created_at': current_time,
                'call_time': current_time,
                
                # Metadata
                'classification_method': 'rule_based',
                'safety_method': 'predefined',
                
                # Post-accident specific actions (if available)
                'post_accident_actions': safety.get('post_accident_actions', []),
                'post_accident_precautions': safety.get('post_accident_precautions', [])
            }
            
            # Store conversation state for follow-up
            call_sid = call_sid or f"hybrid_{time.time()}"
            self.active_conversations[call_sid] = result
            
            # Store in database
            self._store_conversation_async(result, transcript)
            
            logger.info(f"⚡ Hybrid processing completed in {processing_time:.2f}ms")
            logger.info(f"   Category: {result['category']} (P{result['priority']})")
            logger.info(f"   Safety: {len(result['immediate_actions'])} actions, {len(result['safety_precautions'])} precautions")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Hybrid processing failed: {e}")
            return self._get_error_result(start_time)
    
    def _classify_instant(self, transcript: str) -> Dict:
        """Instant rule-based classification"""
        transcript_lower = transcript.lower()
        
        # Find matching emergency type
        category = EmergencyType.OTHER
        priority = 3
        severity = 'MODERATE'
        service = EmergencyService.AMBULANCE
        reasoning = 'General emergency'
        
        for emerg_type, config in self.emergency_keywords.items():
            if any(keyword in transcript_lower for keyword in config['keywords']):
                category = config['category']
                service = config['service']
                
                # Check for high severity indicators
                if any(indicator in transcript_lower for indicator in config['high_severity']):
                    priority = 1
                    severity = 'CRITICAL'
                else:
                    priority = 2
                    severity = 'HIGH'
                break
        
        return {
            'category': category,
            'priority': priority,
            'severity': severity,
            'service': service,
            'reasoning': reasoning
        }
    
    def _store_conversation_async(self, result: Dict, transcript: str):
        """Store conversation result in database asynchronously"""
        try:
            from datetime import datetime
            import json
            
            call_record_data = {
                'call_sid': f"hybrid_{time.time()}",
                'from_number': '',
                'to_number': '',
                'transcript': transcript,
                'emergency_type': classification['category'].value,  # Use enum value for database
                'severity_level': self._map_severity_to_level(classification['priority']),  # Proper LEVEL_X format
                'severity_score': max(0, min(100, (6 - classification['priority']) * 20)),  # Convert priority to score
                'assigned_service': result['assigned_service'],
                'priority': result['priority'],
                'summary': result['reasoning_byte'],
                'confidence': result['confidence'],
                'status': result['status'],  # Use conversation status
                'processing_time_ms': result['processing_time_ms'],
                'call_metadata': json.dumps({
                    'dispatched_service': result['dispatched_service'],
                    'priority_level': result['priority_level'],
                    'response_type': result['response_type'],
                    'classification_method': result['classification_method'],
                    'safety_method': result['safety_method'],
                    'timestamp': result['timestamp'],
                    'call_time': result['call_time'],
                    'immediate_actions': result['immediate_actions'],
                    'safety_precautions': result['safety_precautions'],
                    'what_to_say': result['what_to_say'],
                    'danger_question': result.get('danger_question', ''),
                    'escalated_response': result.get('escalated_response', ''),
                    'conversation_status': result['status'],
                    'frontend_category': frontend_category  # Store frontend category for API responses
                })
            }
            
            database_service.create_call_record(call_record_data)
            
            # Send to frontend via WebSocket
            try:
                from services.websocket_service import websocket_service
                asyncio.create_task(websocket_service.broadcast_call_update({
                    'type': 'emergency_conversation',
                    'data': {
                        'call_sid': call_record_data['call_sid'],
                        'category': frontend_category,  # Use frontend category
                        'emergency_type': classification['category'].value,  # Keep DB enum
                        'priority': result['priority'],
                        'severity': result['priority_level'],
                        'dispatched_service': result['dispatched_service'],
                        'assigned_service': result['assigned_service'],
                        'transcript': transcript,
                        'what_to_say': result['what_to_say'],
                        'immediate_actions': result['immediate_actions'],
                        'safety_precautions': result['safety_precautions'],
                        'timestamp': result['timestamp'],
                        'created_at': result['created_at'],
                        'processing_time_ms': result['processing_time_ms'],
                        'confidence': result['confidence'],
                        'status': result['status'],
                        'danger_question': result.get('danger_question', ''),
                        'escalated_response': result.get('escalated_response', ''),
                        'conversation_status': result['status']
                    }
                }))
                logger.debug("📡 Conversation data sent to frontend via WebSocket")
            except Exception as ws_error:
                logger.warning(f"⚠️ WebSocket broadcast failed: {ws_error}")
            
            logger.debug(f"🗄️ Conversation result stored and sent to frontend")
            
        except Exception as e:
            logger.error(f"❌ Storage error: {e}")
    
    def _get_error_result(self, start_time: float) -> Dict:
        """Get error result"""
        processing_time = (time.time() - start_time) * 1000
        
        return {
            'category': 'Other',
            'priority': 3,
            'reasoning_byte': 'System error during triage',
            'processing_time_ms': processing_time,
            'what_to_say': 'I\'m having trouble understanding. Please stay on the line for assistance.',
            'immediate_actions': ['Stay calm'],
            'safety_precautions': ['Keep phone available'],
            'priority_level': 'MODERATE',
            'response_type': 'error',
            'confidence': 0.3,
            'status': 'ERROR'
        }


# Create singleton instance
hybrid_triage_service = HybridTriageService()
