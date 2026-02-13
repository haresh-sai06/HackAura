import logging
from typing import Dict, List
from models.emergency_schema import EmergencyType, EmergencyService, RoutingResult, SeverityLevel

logger = logging.getLogger(__name__)


class RoutingEngine:
    def __init__(self):
        # Define routing rules based on emergency type
        self.routing_rules = {
            EmergencyType.MEDICAL: EmergencyService.AMBULANCE,
            EmergencyType.FIRE: EmergencyService.FIRE_DEPARTMENT,
            EmergencyType.POLICE: EmergencyService.POLICE,
            EmergencyType.ACCIDENT: EmergencyService.MULTIPLE,  # Ambulance + Police
            EmergencyType.MENTAL_HEALTH: EmergencyService.CRISIS_RESPONSE
        }
        
        # Priority mapping (1-10, where 1 is highest priority)
        self.priority_rules = {
            SeverityLevel.LEVEL_1: 1,  # Critical - highest priority
            SeverityLevel.LEVEL_2: 2,  # High
            SeverityLevel.LEVEL_3: 4,   # Moderate
            SeverityLevel.LEVEL_4: 6    # Low - lower priority
        }
        
        # Multi-service routing details
        self.multi_service_details = {
            EmergencyType.ACCIDENT: {
                "services": [EmergencyService.AMBULANCE, EmergencyService.POLICE],
                "description": "Ambulance and Police required"
            }
        }
    
    def route(self, emergency_type: EmergencyType, severity_level: SeverityLevel) -> RoutingResult:
        """
        Determine appropriate emergency service and priority based on type and severity
        
        Args:
            emergency_type: Classified emergency type
            severity_level: Calculated severity level
            
        Returns:
            RoutingResult with assigned service and priority
        """
        try:
            logger.info(f"Routing emergency: {emergency_type.value} with severity {severity_level.value}")
            
            # Get assigned service based on emergency type
            assigned_service = self.routing_rules.get(emergency_type, EmergencyService.AMBULANCE)
            
            # Get priority based on severity level
            priority = self.priority_rules.get(severity_level, 6)
            
            # Adjust priority for specific scenarios
            priority = self._adjust_priority(emergency_type, severity_level, priority)
            
            # Ensure priority is within valid range
            priority = max(1, min(10, priority))
            
            result = RoutingResult(
                assigned_service=assigned_service,
                priority=priority
            )
            
            logger.info(f"Routing result: {assigned_service.value} with priority {priority}")
            return result
            
        except Exception as e:
            logger.error(f"Routing failed: {e}")
            # Return default routing on error
            return RoutingResult(
                assigned_service=EmergencyService.AMBULANCE,
                priority=6
            )
    
    def _adjust_priority(self, emergency_type: EmergencyType, severity_level: SeverityLevel, base_priority: int) -> int:
        """
        Adjust priority based on specific scenarios
        
        Args:
            emergency_type: Type of emergency
            severity_level: Severity level
            base_priority: Base priority from rules
            
        Returns:
            Adjusted priority
        """
        # Boost priority for certain combinations
        if emergency_type == EmergencyType.FIRE and severity_level == SeverityLevel.LEVEL_1:
            return max(1, base_priority - 1)  # Highest priority for critical fires
        
        if emergency_type == EmergencyType.ACCIDENT and severity_level in [SeverityLevel.LEVEL_1, SeverityLevel.LEVEL_2]:
            return max(1, base_priority - 1)  # High priority for serious accidents
        
        if emergency_type == EmergencyType.MENTAL_HEALTH and severity_level == SeverityLevel.LEVEL_1:
            return max(1, base_priority)  # High priority for critical mental health crises
        
        return base_priority
    
    def get_service_details(self, emergency_type: EmergencyType) -> Dict:
        """
        Get detailed information about required services
        
        Args:
            emergency_type: Type of emergency
            
        Returns:
            Dictionary with service details
        """
        if emergency_type == EmergencyType.ACCIDENT:
            return self.multi_service_details.get(emergency_type, {})
        
        service = self.routing_rules.get(emergency_type, EmergencyService.AMBULANCE)
        return {
            "services": [service],
            "description": f"{service.value} required"
        }
    
    def get_dispatch_message(self, routing_result: RoutingResult, emergency_type: EmergencyType) -> str:
        """
        Generate dispatcher-ready message
        
        Args:
            routing_result: Routing result
            emergency_type: Emergency type
            
        Returns:
            Dispatch message
        """
        if routing_result.assigned_service == EmergencyService.MULTIPLE:
            details = self.get_service_details(emergency_type)
            services = ", ".join([s.value for s in details["services"]])
            return f"Dispatch {services} - Priority {routing_result.priority}"
        else:
            return f"Dispatch {routing_result.assigned_service.value} - Priority {routing_result.priority}"


# Global instance
routing_engine = RoutingEngine()
