"""
TransitIQ Domain Entities & Data Transfer Objects
Defines strictly typed models matching 3NF relational schemas.
"""

from dataclasses import dataclass, asdict
from datetime import datetime, date
from typing import Optional

@dataclass
class Stop:
    stop_id: Optional[int]
    stop_code: str
    stop_name: str
    latitude: float
    longitude: float
    zone_id: int = 1
    wheelchair_accessible: bool = True
    created_at: Optional[datetime] = None

    def to_dict(self):
        return asdict(self)

@dataclass
class Route:
    route_id: Optional[int]
    route_code: str
    route_name: str
    route_type: str  # 'Metro Rail', 'Rapid Bus', 'Express Shuttle', 'Commuter Train'
    origin_stop_id: int
    destination_stop_id: int
    distance_km: float
    base_fare: float
    is_active: bool = True
    created_at: Optional[datetime] = None

    def to_dict(self):
        return asdict(self)

@dataclass
class RouteSegment:
    segment_id: Optional[int]
    route_id: int
    stop_id: int
    stop_sequence: int
    distance_from_start_km: float
    est_travel_time_min: int
    created_at: Optional[datetime] = None

    def to_dict(self):
        return asdict(self)

@dataclass
class Vehicle:
    vehicle_id: Optional[int]
    vehicle_code: str
    vehicle_type: str  # 'Metro Rake', 'Electric Bus', 'CNG Standard Bus', 'Double Decker Bus'
    capacity: int
    fuel_propulsion: str  # 'Electric', 'CNG', 'Diesel-Electric Hybrid', 'Hydrogen Cell'
    operational_status: str  # 'Active', 'Maintenance', 'Depot Reserve', 'Decommissioned'
    commission_date: date
    last_service_date: Optional[date] = None
    created_at: Optional[datetime] = None

    def to_dict(self):
        return asdict(self)

@dataclass
class Trip:
    trip_id: Optional[int]
    trip_code: str
    route_id: int
    vehicle_id: int
    scheduled_departure: datetime
    scheduled_arrival: datetime
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    delay_minutes: int = 0
    trip_status: str = "Scheduled"  # 'Scheduled', 'In-Transit', 'Completed', 'Delayed', 'Cancelled'
    created_at: Optional[datetime] = None

    def to_dict(self):
        return asdict(self)

@dataclass
class PassengerFare:
    transaction_id: Optional[int]
    ticket_reference: str
    trip_id: int
    origin_stop_id: int
    destination_stop_id: int
    passenger_type: str  # 'Standard Adult', 'Student', 'Senior Citizen', 'Commuter Passholder'
    fare_paid: float
    payment_method: str  # 'Transit Smartcard', 'Mobile QR / UPI', 'Contactless EMV', 'Ticket Counter'
    transaction_status: str = "Success"
    boarding_timestamp: Optional[datetime] = None

    def to_dict(self):
        return asdict(self)
