"""
Ultra-Fast Database Integration Service
Handles storage of ultra-fast triage results in existing database
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy import func
from services.database_service import database_service
from models.database import EmergencyType, SeverityLevel, CallStatus, EmergencyService, CallRecord

logger = logging.getLogger(__name__)


class UltraFastDatabaseService:
    """Service to integrate ultra-fast triage with existing database"""
    
    def __init__(self):
        self.db_service = database_service
        self.category_mapping = {
            'Medical': EmergencyType.MEDICAL,
            'Fire': EmergencyType.FIRE,
            'Crime': EmergencyType.POLICE,
            'Other': EmergencyType.OTHER
        }
        
        self.priority_mapping = {
            1: SeverityLevel.LEVEL_1,  # Critical
            2: SeverityLevel.LEVEL_2,  # High
            3: SeverityLevel.LEVEL_3,  # Moderate
            4: SeverityLevel.LEVEL_4,  # Low
            5: SeverityLevel.LEVEL_4   # Very Low -> Low
        }
        
        self.service_mapping = {
            'Medical': EmergencyService.AMBULANCE,
            'Fire': EmergencyService.FIRE_DEPARTMENT,
            'Crime': EmergencyService.POLICE,
            'Other': EmergencyService.AMBULANCE  # Default to ambulance
        }
        
        logger.info("🗄️ Ultra-Fast Database Service initialized")
    
    def store_ultra_fast_result(self, ultra_fast_result: Dict[str, Any], call_data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Store ultra-fast triage result in existing database
        
        Args:
            ultra_fast_result: Result from ultra-fast service
            call_data: Additional call metadata (call_sid, from_number, etc.)
            
        Returns:
            True if successfully stored, False otherwise
        """
        try:
            # Map ultra-fast categories to existing enums
            category = ultra_fast_result.get('category', 'Other')
            priority = ultra_fast_result.get('priority', 3)
            
            emergency_type = self.category_mapping.get(category, EmergencyType.OTHER)
            severity_level = self.priority_mapping.get(priority, SeverityLevel.LEVEL_3)
            assigned_service = self.service_mapping.get(category, EmergencyService.AMBULANCE)
            
            # Prepare call record data
            call_record_data = {
                'call_sid': call_data.get('call_sid') if call_data else f"ultra_fast_{datetime.now().timestamp()}",
                'from_number': call_data.get('from_number', '') if call_data else '',
                'to_number': call_data.get('to_number', '') if call_data else '',
                'transcript': call_data.get('transcript', '') if call_data else '',
                
                # Map ultra-fast results to existing schema
                'emergency_type': emergency_type.value,
                'severity_level': severity_level.value,
                'severity_score': max(0, min(100, (6 - priority) * 20)),  # Convert priority 1-5 to score 100-20
                'assigned_service': assigned_service.value,
                'priority': priority,
                'location': call_data.get('location') if call_data else None,
                'summary': ultra_fast_result.get('reasoning_byte', ''),
                'confidence': 0.8,  # High confidence for rule-based
                'status': CallStatus.PENDING.value,
                
                # Processing metadata
                'processing_time_ms': ultra_fast_result.get('processing_time_ms', 0.0),
                'created_at': datetime.utcnow()
            }
            
            # Store in database
            call_record = self.db_service.create_call_record(call_record_data)
            
            logger.info(f"✅ Ultra-fast result stored: {category} (P{priority}) -> {emergency_type.value}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to store ultra-fast result: {e}")
            return False
    
    def get_recent_ultra_fast_calls(self, limit: int = 50) -> list:
        """
        Get recent ultra-fast processed calls
        
        Args:
            limit: Maximum number of calls to return
            
        Returns:
            List of call records
        """
        try:
            session = self.db_service.get_session()
            
            # Get recent calls with ultra-fast call_sid pattern
            calls = session.query(CallRecord)\
                .filter(CallRecord.call_sid.like('ultra_fast_%'))\
                .order_by(CallRecord.created_at.desc())\
                .limit(limit)\
                .all()
            
            # Convert to dict format
            results = []
            for call in calls:
                results.append({
                    'id': call.id,
                    'call_sid': call.call_sid,
                    'from_number': call.from_number,
                    'emergency_type': call.emergency_type.value,
                    'severity_level': call.severity_level.value,
                    'priority': call.priority,
                    'summary': call.summary,
                    'processing_time_ms': call.processing_time_ms,
                    'created_at': call.created_at.isoformat() if call.created_at else None
                })
            
            session.close()
            return results
            
        except Exception as e:
            logger.error(f"❌ Failed to get ultra-fast calls: {e}")
            return []
    
    def get_ultra_fast_stats(self) -> Dict[str, Any]:
        """
        Get statistics for ultra-fast processed calls
        
        Returns:
            Statistics dictionary
        """
        try:
            session = self.db_service.get_session()
            
            # Count ultra-fast calls
            total_calls = session.query(CallRecord)\
                .filter(CallRecord.call_sid.like('ultra_fast_%'))\
                .count()
            
            # Average processing time
            avg_time = session.query(func.avg(CallRecord.processing_time_ms))\
                .filter(CallRecord.call_sid.like('ultra_fast_%'))\
                .scalar() or 0.0
            
            # Category distribution
            category_stats = {}
            for category in ['Medical', 'Fire', 'Crime', 'Other']:
                count = session.query(CallRecord)\
                    .filter(
                        CallRecord.call_sid.like('ultra_fast_%'),
                        CallRecord.emergency_type == self.category_mapping.get(category, EmergencyType.OTHER)
                    )\
                    .count()
                category_stats[category.lower()] = count
            
            session.close()
            
            return {
                'total_ultra_fast_calls': total_calls,
                'avg_processing_time_ms': float(avg_time),
                'category_distribution': category_stats,
                'performance_rating': 'ULTRA-FAST (<1ms)' if avg_time < 1 else 'FAST'
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get ultra-fast stats: {e}")
            return {
                'total_ultra_fast_calls': 0,
                'avg_processing_time_ms': 0.0,
                'category_distribution': {},
                'performance_rating': 'UNKNOWN'
            }


# Create singleton instance
ultra_fast_db_service = UltraFastDatabaseService()
