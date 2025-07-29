# models.py - Data Models and Classes
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class FacilityType(Enum):
    HUB = "hub"
    STATION = "station"
    RECEIVING_POINT = "receiving_point"

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class MessagePriority(Enum):
    NORMAL = "normal"
    MEDIUM = "medium"
    HIGH = "high"

class EquipmentStatus(Enum):
    OPERATIONAL = "Operational"
    MAINTENANCE = "Maintenance"
    DOWN = "Down"
    REDUCED_CAPACITY = "Reduced Capacity"

@dataclass
class Facility:
    id: Optional[int]
    name: str
    location: str
    facility_type: str
    status: str = "active"
    max_capacity: int = 1000
    current_load: int = 0

@dataclass
class FacilityMetrics:
    facility_id: int
    staffing_level: int
    productivity_rate: float
    equipment_status: str
    downtime_minutes: int = 0
    timestamp: Optional[str] = None

@dataclass
class WeatherData:
    location: str
    temperature: float
    conditions: str
    wind_speed: float
    visibility: str
    alerts: List[str]

@dataclass
class TrafficData:
    route_id: str
    congestion_level: str
    incidents: List[str]
    estimated_delay_minutes: int
    alternative_routes: List[str]

@dataclass
class Alert:
    id: Optional[int]
    facility_id: int
    alert_type: str
    message: str
    severity: str = AlertSeverity.INFO.value
    resolved: bool = False
    created_at: Optional[str] = None

@dataclass
class Message:
    id: Optional[int]
    from_facility_id: int
    to_facility_id: int
    message: str
    priority: str = MessagePriority.NORMAL.value
    status: str = "sent"
    created_at: Optional[str] = None

@dataclass
class Route:
    id: Optional[int]
    from_facility_id: int
    to_facility_id: int
    distance_miles: int
    estimated_time_hours: float
    status: str = "active"

@dataclass
class Recommendation:
    type: str
    priority: str
    source_facility: Optional[str] = None
    location: Optional[str] = None
    reason: str = ""
    suggested_alternatives: Optional[List[str]] = None
    suggested_action: Optional[str] = None
    estimated_impact: str = ""
