"""
Robust enum handling utilities for case-insensitive operations
"""

from typing import Union, Type, Optional
from enum import Enum
import logging

# Import the enums we need to handle
from models.database import EmergencyType, SeverityLevel, CallStatus, EmergencyService

logger = logging.getLogger(__name__)

class EnumHandler:
    """Handles enum conversions with case-insensitive support"""
    
    @staticmethod
    def normalize_enum_value(value: Union[str, Enum], enum_class: Type[Enum]) -> Enum:
        """
        Convert a string or enum to the proper enum value, handling case differences
        
        Args:
            value: String or enum value to normalize
            enum_class: The target enum class
            
        Returns:
            Proper enum instance
            
        Raises:
            ValueError: If the value cannot be converted to the enum
        """
        if isinstance(value, enum_class):
            return value
            
        if isinstance(value, str):
            # Try exact match first
            try:
                return enum_class(value.upper())
            except ValueError:
                pass
            
            # Try case-insensitive match
            value_upper = value.upper()
            for enum_value in enum_class:
                if enum_value.value == value_upper:
                    return enum_value
            
            # Try partial match for common variations
            value_lower = value.lower()
            for enum_value in enum_class:
                enum_lower = enum_value.value.lower()
                if enum_lower == value_lower:
                    return enum_value
                # Handle common variations
                if value_lower in enum_lower or enum_lower in value_lower:
                    return enum_value
            
            raise ValueError(f"Cannot convert '{value}' to {enum_class.__name__}")
        
        raise ValueError(f"Unsupported type for enum conversion: {type(value)}")
    
    @staticmethod
    def safe_get_enum_value(value: Union[str, Enum, None], enum_class: Type[Enum], default: Optional[Enum] = None) -> Optional[Enum]:
        """
        Safely convert to enum with fallback to default value
        
        Args:
            value: Value to convert
            enum_class: Target enum class
            default: Default value if conversion fails
            
        Returns:
            Enum instance or default value
        """
        if value is None:
            return default
            
        try:
            return EnumHandler.normalize_enum_value(value, enum_class)
        except ValueError as e:
            logger.warning(f"Enum conversion failed: {e}. Using default: {default}")
            return default
    
    @staticmethod
    def get_enum_mapping(enum_class: Type[Enum]) -> dict:
        """
        Get a mapping of various case variations to enum values
        
        Args:
            enum_class: Enum class to map
            
        Returns:
            Dictionary mapping string variations to enum values
        """
        mapping = {}
        
        for enum_value in enum_class:
            original = enum_value.value
            upper = original.upper()
            lower = original.lower()
            
            # Add all variations
            mapping[original] = enum_value
            mapping[upper] = enum_value
            mapping[lower] = enum_value
            
            # Add common variations
            if '_' in original:
                # Replace underscores with spaces
                spaced = original.replace('_', ' ')
                mapping[spaced] = enum_value
                mapping[spaced.upper()] = enum_value
                mapping[spaced.lower()] = enum_value
                mapping[spaced.replace(' ', '')] = enum_value  # No spaces
        
        return mapping

# Pre-built mappings for common enums
EMERGENCY_TYPE_MAPPING = EnumHandler.get_enum_mapping(EmergencyType)
SEVERITY_LEVEL_MAPPING = EnumHandler.get_enum_mapping(SeverityLevel)
CALL_STATUS_MAPPING = EnumHandler.get_enum_mapping(CallStatus)
EMERGENCY_SERVICE_MAPPING = EnumHandler.get_enum_mapping(EmergencyService)

def normalize_emergency_type(value: Union[str, Enum]) -> EmergencyType:
    """Normalize emergency type with case-insensitive support"""
    return EnumHandler.normalize_enum_value(value, EmergencyType)

def normalize_severity_level(value: Union[str, Enum]) -> SeverityLevel:
    """Normalize severity level with case-insensitive support"""
    return EnumHandler.normalize_enum_value(value, SeverityLevel)

def normalize_call_status(value: Union[str, Enum]) -> CallStatus:
    """Normalize call status with case-insensitive support"""
    return EnumHandler.normalize_enum_value(value, CallStatus)

def normalize_emergency_service(value: Union[str, Enum]) -> EmergencyService:
    """Normalize emergency service with case-insensitive support"""
    return EnumHandler.normalize_enum_value(value, EmergencyService)
