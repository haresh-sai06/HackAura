import logging
from typing import Dict, Any
from models.emergency_schema import EmergencyType, SeverityLevel, EmergencyService, RoutingResult

logger = logging.getLogger(__name__)

class RoutingEngine:
    def __init__(self):
        # Define routing rules based on emergency type
        self.routing_rules = {
            EmergencyType.MEDICAL: EmergencyService.AMBULANCE,
            EmergencyType.FIRE: EmergencyService.FIRE_DEPARTMENT,
            EmergencyType.POLICE: EmergencyService.POLICE,
            EmergencyType.ACCIDENT: EmergencyService.MULTIPLE,  # Ambulance + Police
            EmergencyType.MENTAL_HEALTH: EmergencyService.CRISIS_RESPONSE,
            EmergencyType.OTHER: EmergencyService.POLICE
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
    
    def route_emergency(self, emergency_type: EmergencyType, severity_level: SeverityLevel) -> RoutingResult:
        """
        Route emergency to appropriate service based on type and severity
        
        Args:
            emergency_type: Type of emergency
            severity_level: Severity level of emergency
            
        Returns:
            RoutingResult with assigned service and priority
        """
        logger.debug(f"🚑 ROUTING ENGINE STARTING")
        logger.debug(f"   Emergency Type: {emergency_type.value}")
        logger.debug(f"   Severity Level: {severity_level.value}")
        
        # Base routing by emergency type
        base_routing = {
            EmergencyType.MEDICAL: EmergencyService.AMBULANCE,
            EmergencyType.FIRE: EmergencyService.FIRE_DEPARTMENT,
            EmergencyType.POLICE: EmergencyService.POLICE,
            EmergencyType.ACCIDENT: EmergencyService.MULTIPLE,
            EmergencyType.MENTAL_HEALTH: EmergencyService.CRISIS_RESPONSE,
            EmergencyType.OTHER: EmergencyService.POLICE
        }
        
        assigned_service = base_routing.get(emergency_type, EmergencyService.POLICE)
        
        logger.debug(f"   🎯 BASE ROUTING:")
        logger.debug(f"      Type -> Service: {emergency_type.value} -> {assigned_service.value}")
        
        # Adjust for multi-service emergencies
        if emergency_type == EmergencyType.ACCIDENT:
            logger.debug(f"      🚗 ACCIDENT DETECTED - Multiple services needed")
            if severity_level in [SeverityLevel.LEVEL_1, SeverityLevel.LEVEL_2]:
                logger.debug(f"         High severity accident -> Ambulance + Fire + Police")
                assigned_service = EmergencyService.MULTIPLE
            else:
                logger.debug(f"         Low severity accident -> Police + Ambulance")
                assigned_service = EmergencyService.MULTIPLE
        
        # Calculate priority based on severity
        priority_mapping = {
            SeverityLevel.LEVEL_1: 1,  # Critical - highest priority
            SeverityLevel.LEVEL_2: 2,  # High
            SeverityLevel.LEVEL_3: 4,  # Moderate
            SeverityLevel.LEVEL_4: 6   # Low - lowest priority
        }
        
        base_priority = priority_mapping.get(severity_level, 4)
        
        logger.debug(f"   📊 PRIORITY CALCULATION:")
        logger.debug(f"      Severity -> Base Priority: {severity_level.value} -> {base_priority}")
        
        # Adjust priority based on emergency type
        if emergency_type == EmergencyType.MEDICAL:
            if severity_level == SeverityLevel.LEVEL_1:
                priority = 1
                logger.debug(f"      🏥 Critical medical -> Priority 1 (highest)")
            else:
                priority = base_priority - 1
                logger.debug(f"      🏥 Medical emergency -> Priority {priority} (elevated)")
        elif emergency_type == EmergencyType.FIRE:
            priority = base_priority - 1
            logger.debug(f"      🔥 Fire emergency -> Priority {priority} (elevated)")
        elif emergency_type == EmergencyType.POLICE:
            if severity_level == SeverityLevel.LEVEL_1:
                priority = 1
                logger.debug(f"      👮 Critical police -> Priority 1 (highest)")
            else:
                priority = base_priority
                logger.debug(f"      👮 Police emergency -> Priority {priority} (standard)")
        else:
            priority = base_priority
            logger.debug(f"      📋 Standard routing -> Priority {priority}")
        
        # Ensure priority is within valid range
        priority = max(1, min(10, priority))
        
        logger.debug(f"   🎯 FINAL ROUTING DECISION:")
        logger.debug(f"      Assigned Service: {assigned_service.value}")
        logger.debug(f"      Final Priority: {priority}")
        logger.debug(f"      Priority Range: 1 (highest) to 10 (lowest)")
        
        result = RoutingResult(
            assigned_service=assigned_service,
            priority=priority
        )
        
        logger.info(f"🚑 ROUTING COMPLETE: {assigned_service.value} (priority: {priority})")
        return result
    
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
