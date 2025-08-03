# external_apis.py - External API Providers with Fallback
import random
import math
from typing import Optional, List
from dataclasses import asdict
from datetime import datetime, timedelta
from core.models import WeatherData, TrafficData, FacilityMetrics


class MockWeatherProvider:
    """Mock weather data provider with fallback capability"""

    def __init__(self, is_primary=True):
        self.is_primary = is_primary
        self.failure_rate = 0.1 if is_primary else 0.05  # Primary fails more often
        self.provider_name = (
            "Primary Weather API" if is_primary else "Secondary Weather API"
        )

    def get_weather_data(self, location: str) -> Optional[WeatherData]:
        """Get weather data for a location"""
        # Simulate API failure
        if random.random() < self.failure_rate:
            return None

        conditions = ["Clear", "Cloudy", "Rain", "Snow", "Fog", "Storm"]
        weather_alerts = []

        # Generate weather alerts based on conditions
        condition = random.choice(conditions)
        if condition in ["Snow", "Storm"]:
            weather_alerts.append(f"Severe weather warning: {condition}")
        if condition == "Fog":
            weather_alerts.append("Visibility reduced due to fog")

        return WeatherData(
            location=location,
            temperature=random.uniform(-10, 35),
            conditions=condition,
            wind_speed=random.uniform(0, 25),
            visibility="Good" if condition not in ["Fog", "Storm"] else "Poor",
            alerts=weather_alerts,
        )


class MockTrafficProvider:
    """Mock highway closure and incidents provider"""

    def __init__(self, is_primary=True):
        self.is_primary = is_primary
        self.failure_rate = 0.15 if is_primary else 0.08
        self.provider_name = (
            "Primary Highway API" if is_primary else "Secondary Highway API"
        )

        # Major logistics highways - focusing on 3 most critical corridors
        self.highways = {
            "I-80 Chicago↔Denver": "I-80 Chicago → Denver Corridor",
            "I-75 Chicago↔Atlanta": "I-75 Chicago → Atlanta Corridor",
            "I-10 Phoenix↔Miami": "I-10 Phoenix → Miami Corridor",
        }

    def get_traffic_data(self, route_id: str) -> Optional[TrafficData]:
        """Get highway closure and incident data"""
        # Simulate API failure
        if random.random() < self.failure_rate:
            return None

        # Highway closure scenarios with route-specific incidents
        route_specific_incidents = {
            "I-80 Chicago↔Denver": [
                "Winter weather closure near Des Moines",
                "Bridge construction in Nebraska - single lane",
                "High wind restrictions for high-profile vehicles",
                "Oversize load convoy - 30 min delays",
            ],
            "I-75 Chicago↔Atlanta": [
                "Construction in Kentucky - lane restrictions",
                "Fog conditions in Tennessee valleys",
                "Multi-vehicle accident near Cincinnati",
                "Road work in Georgia - expect delays",
            ],
            "I-10 Phoenix↔Miami": [
                "Dust storm warnings in Arizona",
                "Hurricane evacuation route - heavy traffic",
                "Bridge maintenance in Louisiana",
                "Flooding concerns in Texas panhandle",
            ],
        }

        incidents = []
        delay = 0
        severity = "Clear"

        # Realistic highway closure probability
        issue_chance = random.random()

        if issue_chance < 0.05:  # 5% chance of major closure
            incidents.append("FULL HIGHWAY CLOSURE - Both directions closed")
            severity = "Severe"
            delay = random.randint(240, 480)  # 4-8 hours
        elif issue_chance < 0.12:  # 7% chance of significant issue
            route_incidents = route_specific_incidents.get(
                route_id,
                [
                    "Construction zone delays",
                    "Weather-related restrictions",
                    "Accident with lane closures",
                ],
            )
            incidents.append(random.choice(route_incidents))
            severity = "Heavy"
            delay = random.randint(30, 120)  # 30min - 2 hours
        elif issue_chance < 0.25:  # 13% chance of minor issue
            incidents.append(
                random.choice(
                    [
                        "Lane restrictions - maintain speed",
                        "Temporary speed reduction",
                        "Shoulder work - no truck restrictions",
                    ]
                )
            )
            severity = "Moderate"
            delay = random.randint(5, 30)  # 5-30 minutes

        # Generate meaningful alternative routes based on specific corridor
        alternatives = []
        highway_name = self.highways.get(route_id, f"Route {route_id}")

        corridor_alternatives = {
            "I-80 Chicago↔Denver": [
                "I-76 through Pennsylvania/Ohio (longer)",
                "I-70 through Kansas (southern route)",
                "Rail freight via BNSF recommended",
            ],
            "I-75 Chicago↔Atlanta": [
                "I-65 through Alabama (western route)",
                "I-77 through West Virginia (eastern route)",
                "CSX rail service available",
            ],
            "I-10 Phoenix↔Miami": [
                "I-40 to I-75 (northern route)",
                "I-20 through Texas/Louisiana",
                "Consider air freight for urgent shipments",
            ],
        }

        if incidents:
            if "CLOSURE" in incidents[0]:
                alternatives = corridor_alternatives.get(
                    route_id,
                    [
                        "Major detour required (add 4-8 hours)",
                        "Rail freight strongly recommended",
                        "Delay all non-urgent shipments",
                    ],
                )
            elif severity == "Heavy":
                alternatives = corridor_alternatives.get(
                    route_id,
                    [
                        "State route alternate available",
                        "Off-peak travel recommended",
                        "Split shipments to reduce impact",
                    ],
                )
            else:
                alternatives = [
                    "Monitor conditions hourly",
                    "Allow extra 30-60 minutes",
                    "Update customer delivery expectations",
                ]

        return TrafficData(
            route_id=highway_name,
            congestion_level=severity,
            incidents=incidents,
            estimated_delay_minutes=delay,
            alternative_routes=alternatives,
        )


class MockInternalDataProvider:
    """Mock internal company data provider with realistic progression"""

    def __init__(self):
        self.failure_rate = 0.05  # 5% chance of data unavailability
        self.facility_states = {}  # Persistent state for each facility
        self.last_update_time = {}  # Track last update time per facility

    def get_facility_metrics(self, facility_id: int, facility_type: str = "station") -> Optional[FacilityMetrics]:
        """Get metrics for a facility with realistic time-based progression"""
        # Simulate occasional data unavailability
        if random.random() < self.failure_rate:
            return None

        current_time = datetime.now()
        
        # Initialize facility state if first time
        if facility_id not in self.facility_states:
            self._initialize_facility_state(facility_id, facility_type)
            
        # Get current state
        state = self.facility_states[facility_id]
        last_update = self.last_update_time.get(facility_id, current_time - timedelta(hours=1))
        hours_since_update = (current_time - last_update).total_seconds() / 3600
        
        # Update state based on time progression
        self._update_facility_state(facility_id, facility_type, hours_since_update)
        
        # Update last update time
        self.last_update_time[facility_id] = current_time
        
        # Generate timestamp with realistic reporting delay
        minutes_offset = (facility_id * 17) % 60  # Spread across hour
        timestamp = (current_time - timedelta(minutes=minutes_offset)).strftime("%Y-%m-%d %H:%M:%S")

        return FacilityMetrics(
            facility_id=facility_id,
            staffing_level=state['staffing_level'],
            productivity_rate=state['productivity_rate'],
            equipment_status=state['equipment_status'],
            downtime_minutes=state['downtime_minutes'],
            delivery_timeliness=state['delivery_timeliness'],
            timestamp=timestamp
        )
    
    def _initialize_facility_state(self, facility_id: int, facility_type: str):
        """Initialize realistic starting state for a facility"""
        if facility_type == "hub":
            base_staffing = random.randint(150, 250)  # More stable initial staffing
            base_productivity = random.uniform(0.85, 1.05)
            base_timeliness = random.uniform(90.0, 96.0)
        else:  # station
            base_staffing = random.randint(15, 25)
            base_productivity = random.uniform(0.88, 1.02)
            base_timeliness = random.uniform(92.0, 98.0)
        
        # Equipment status - most start operational
        equipment_statuses = ["Operational", "Operational", "Operational", "Maintenance"]
        equipment_status = random.choice(equipment_statuses)
        
        self.facility_states[facility_id] = {
            'staffing_level': base_staffing,
            'productivity_rate': base_productivity,
            'equipment_status': equipment_status,
            'delivery_timeliness': base_timeliness,
            'downtime_minutes': 0,
            'equipment_change_cooldown': 0,  # Hours until equipment can change status
            'staffing_trend': 0,  # Tracks gradual staffing changes
            'productivity_trend': 0,  # Tracks gradual productivity changes
        }
    
    def _update_facility_state(self, facility_id: int, facility_type: str, hours_elapsed: float):
        """Update facility state with realistic progression over time"""
        state = self.facility_states[facility_id]
        
        # Reduce cooldowns
        state['equipment_change_cooldown'] = max(0, state['equipment_change_cooldown'] - hours_elapsed)
        
        # Equipment status changes (rare and with cooldowns)
        if state['equipment_change_cooldown'] <= 0:
            self._update_equipment_status(state, hours_elapsed)
        
        # Gradual staffing changes (realistic HR dynamics)
        self._update_staffing_level(state, facility_type, hours_elapsed)
        
        # Productivity changes (affected by staffing and equipment)
        self._update_productivity(state, facility_type, hours_elapsed)
        
        # Timeliness changes (affected by productivity and equipment)
        self._update_timeliness(state, facility_type, hours_elapsed)
        
        # Update downtime
        self._update_downtime(state, hours_elapsed)
    
    def _update_equipment_status(self, state: dict, hours_elapsed: float):
        """Update equipment status with realistic transitions"""
        current_status = state['equipment_status']
        
        # Equipment status transition probabilities (per hour)
        if current_status == "Operational":
            # Small chance of issues developing
            if random.random() < 0.001 * hours_elapsed:  # 0.1% per hour
                if random.random() < 0.7:
                    state['equipment_status'] = "Maintenance"
                    state['equipment_change_cooldown'] = random.uniform(4, 12)  # 4-12 hours maintenance
                else:
                    state['equipment_status'] = "Down"
                    state['equipment_change_cooldown'] = random.uniform(1, 6)  # 1-6 hours down
                    
        elif current_status == "Maintenance":
            # Chance maintenance completes
            if random.random() < 0.15 * hours_elapsed:  # 15% per hour
                state['equipment_status'] = "Operational"
                state['equipment_change_cooldown'] = random.uniform(24, 72)  # 1-3 days before next issue
                
        elif current_status == "Down":
            # Higher chance of repair completion
            if random.random() < 0.25 * hours_elapsed:  # 25% per hour
                if random.random() < 0.8:
                    state['equipment_status'] = "Operational" 
                    state['equipment_change_cooldown'] = random.uniform(12, 48)  # 0.5-2 days
                else:
                    state['equipment_status'] = "Maintenance"  # Needs maintenance after repair
                    state['equipment_change_cooldown'] = random.uniform(2, 8)  # 2-8 hours maintenance
    
    def _update_staffing_level(self, state: dict, facility_type: str, hours_elapsed: float):
        """Update staffing with realistic HR dynamics"""
        current_staffing = state['staffing_level']
        trend = state['staffing_trend']
        
        # Staffing changes are rare and gradual
        if hours_elapsed >= 8:  # Only check for changes every 8+ hours (shift changes)
            # Small chance of staffing changes
            if random.random() < 0.05:  # 5% chance per 8-hour period
                if facility_type == "hub":
                    # Hubs have more staffing volatility
                    trend_change = random.uniform(-2, 2)  # People per hour trend change
                    state['staffing_trend'] = max(-5, min(5, trend + trend_change))
                else:
                    # Stations have more stable staffing
                    trend_change = random.uniform(-0.5, 0.5)
                    state['staffing_trend'] = max(-2, min(2, trend + trend_change))
        
        # Apply gradual staffing changes
        if trend != 0:
            staffing_change = trend * hours_elapsed
            new_staffing = current_staffing + staffing_change
            
            # Staffing bounds
            if facility_type == "hub":
                new_staffing = max(80, min(350, new_staffing))  # Hub bounds
            else:
                new_staffing = max(8, min(35, new_staffing))    # Station bounds
            
            state['staffing_level'] = int(new_staffing)
            
            # Trend decay (staffing changes eventually stabilize)
            state['staffing_trend'] *= 0.95
    
    def _update_productivity(self, state: dict, facility_type: str, hours_elapsed: float):
        """Update productivity based on staffing and equipment"""
        current_productivity = state['productivity_rate']
        
        # Equipment impact on productivity
        equipment_multiplier = {
            "Operational": 1.0,
            "Maintenance": 0.7,
            "Down": 0.1,
            "Reduced Capacity": 0.6
        }.get(state['equipment_status'], 1.0)
        
        # Staffing impact (optimal staffing = baseline productivity)
        if facility_type == "hub":
            optimal_staffing = 200
            staffing_ratio = state['staffing_level'] / optimal_staffing
        else:
            optimal_staffing = 20
            staffing_ratio = state['staffing_level'] / optimal_staffing
        
        # Productivity decreases if over/understaffed
        if staffing_ratio < 0.7:
            staffing_multiplier = 0.6 + (staffing_ratio * 0.4)  # Understaffed penalty
        elif staffing_ratio > 1.3:
            staffing_multiplier = 1.0 - ((staffing_ratio - 1.3) * 0.3)  # Overstaffed penalty
        else:
            staffing_multiplier = 0.9 + (staffing_ratio * 0.1)  # Optimal range
        
        # Calculate target productivity
        base_productivity = 0.95 if facility_type == "hub" else 0.92
        target_productivity = base_productivity * equipment_multiplier * staffing_multiplier
        
        # Gradual change toward target (productivity changes slowly)
        change_rate = 0.1 * hours_elapsed  # 10% of gap per hour
        productivity_gap = target_productivity - current_productivity
        new_productivity = current_productivity + (productivity_gap * change_rate)
        
        # Bounds
        state['productivity_rate'] = max(0.1, min(1.3, new_productivity))
    
    def _update_timeliness(self, state: dict, facility_type: str, hours_elapsed: float):
        """Update delivery timeliness based on productivity and equipment"""
        current_timeliness = state['delivery_timeliness']
        
        # Timeliness is affected by productivity and equipment
        productivity_factor = min(1.0, state['productivity_rate'])  # Cap at 100%
        equipment_factor = {
            "Operational": 1.0,
            "Maintenance": 0.85,
            "Down": 0.3,
            "Reduced Capacity": 0.75
        }.get(state['equipment_status'], 1.0)
        
        # Base timeliness targets
        base_timeliness = 96.0 if facility_type == "hub" else 94.0
        target_timeliness = base_timeliness * productivity_factor * equipment_factor
        
        # Gradual change (timeliness responds faster than productivity)
        change_rate = 0.2 * hours_elapsed  # 20% of gap per hour
        timeliness_gap = target_timeliness - current_timeliness
        new_timeliness = current_timeliness + (timeliness_gap * change_rate)
        
        # Bounds
        state['delivery_timeliness'] = max(60.0, min(99.9, new_timeliness))
    
    def _update_downtime(self, state: dict, hours_elapsed: float):
        """Update downtime minutes based on equipment status"""
        if state['equipment_status'] == "Down":
            # Accumulate downtime while equipment is down
            state['downtime_minutes'] += int(hours_elapsed * 60)
            state['downtime_minutes'] = min(480, state['downtime_minutes'])  # Cap at 8 hours
        elif state['equipment_status'] == "Operational":
            # Gradually reduce downtime counter when operational
            reduction = int(hours_elapsed * 30)  # Reduce by 30 min per hour
            state['downtime_minutes'] = max(0, state['downtime_minutes'] - reduction)
        # Maintenance status keeps downtime stable


# Global data providers with fallback
primary_weather = MockWeatherProvider(is_primary=True)
secondary_weather = MockWeatherProvider(is_primary=False)
primary_traffic = MockTrafficProvider(is_primary=True)
secondary_traffic = MockTrafficProvider(is_primary=False)
internal_data = MockInternalDataProvider()


class DataService:
    """Service implementing fallback mechanisms for external APIs"""

    @staticmethod
    def get_weather_with_fallback(location: str) -> Optional[WeatherData]:
        """Get weather data with fallback to secondary provider"""
        # Try primary provider first
        data = primary_weather.get_weather_data(location)
        if data:
            return data

        # Fall back to secondary provider
        data = secondary_weather.get_weather_data(location)
        if data:
            # Log fallback usage (in real app, this would go to logging system)
            print(f"WARNING: Using secondary weather provider for {location}")
            return data

        print(f"ERROR: All weather providers failed for {location}")
        return None

    @staticmethod
    def get_traffic_with_fallback(route_id: str) -> Optional[TrafficData]:
        """Get traffic data with fallback to secondary provider"""
        # Try primary provider first
        data = primary_traffic.get_traffic_data(route_id)
        if data:
            return data

        # Fall back to secondary provider
        data = secondary_traffic.get_traffic_data(route_id)
        if data:
            print(f"WARNING: Using secondary traffic provider for route {route_id}")
            return data

        print(f"ERROR: All traffic providers failed for route {route_id}")
        return None

    @staticmethod
    def get_facility_metrics(facility_id: int, facility_type: str = "station") -> Optional[FacilityMetrics]:
        """Get facility metrics from internal provider"""
        return internal_data.get_facility_metrics(facility_id, facility_type)


# Geographical proximity system for better facility recommendations
CITY_COORDINATES = {
    # Major hubs
    "Chicago, IL": (41.8781, -87.6298),
    "Los Angeles, CA": (34.0522, -118.2437),
    "Atlanta, GA": (33.7490, -84.3880),
    "Dallas, TX": (32.7767, -96.7970),
    "Newark, NJ": (40.7357, -74.1724),
    "Denver, CO": (39.7392, -104.9903),
    "Memphis, TN": (35.1495, -90.0490),
    "Phoenix, AZ": (33.4484, -112.0740),
    "Seattle, WA": (47.6062, -122.3321),
    "Miami, FL": (25.7617, -80.1918),
    "Indianapolis, IN": (39.7684, -86.1581),
    "Kansas City, MO": (39.0997, -94.5786),
    "Charlotte, NC": (35.2271, -80.8431),
    "Cincinnati, OH": (39.1031, -84.5120),
    "Portland, OR": (45.5152, -122.6784),
    "Houston, TX": (29.7604, -95.3698),
    "Philadelphia, PA": (39.9526, -75.1652),
    "Salt Lake City, UT": (40.7608, -111.8910),
    "Nashville, TN": (36.1627, -86.7816),
    "Raleigh, NC": (35.7796, -78.6382),
    
    # Chicago area stations
    "Milwaukee, WI": (43.0389, -87.9065),
    "Madison, WI": (43.0731, -89.4012),
    "Rockford, IL": (42.2711, -89.0940),
    "Peoria, IL": (40.6936, -89.5890),
    
    # Los Angeles area stations
    "San Diego, CA": (32.7157, -117.1611),
    "Riverside, CA": (33.9533, -117.3962),
    "Bakersfield, CA": (35.3733, -119.0187),
    "Fresno, CA": (36.7378, -119.7871),
    "Ventura, CA": (34.2746, -119.2290),
    
    # Atlanta area stations
    "Birmingham, AL": (33.5186, -86.8104),
    "Columbia, SC": (34.0007, -81.0348),
    "Savannah, GA": (32.0835, -81.0998),
    "Augusta, GA": (33.4735, -82.0105),
    
    # Dallas area stations
    "San Antonio, TX": (29.4241, -98.4936),
    "Austin, TX": (30.2672, -97.7431),
    "Waco, TX": (31.5494, -97.1467),
    "Tyler, TX": (32.3513, -95.3011),
    
    # New York area stations
    "Albany, NY": (42.6526, -73.7562),
    "Trenton, NJ": (40.2206, -74.7565),
    "Hartford, CT": (41.7658, -72.6734),
    "Allentown, PA": (40.6023, -75.4714),
    
    # Denver area stations
    "Colorado Springs, CO": (38.8339, -104.8214),
    "Boulder, CO": (40.0150, -105.2705),
    "Fort Collins, CO": (40.5853, -105.0844),
    "Grand Junction, CO": (39.0639, -108.5506),
    
    # Memphis area stations
    "Little Rock, AR": (34.7465, -92.2896),
    "Jackson, MS": (32.2988, -90.1848),
    "Tupelo, MS": (34.2576, -88.7034),
    
    # Phoenix area stations
    "Tucson, AZ": (32.2226, -110.9747),
    "Flagstaff, AZ": (35.1983, -111.6513),
    "Yuma, AZ": (32.6927, -114.6277),
    
    # Seattle area stations
    "Spokane, WA": (47.6587, -117.4260),
    "Tacoma, WA": (47.2529, -122.4443),
    "Bellingham, WA": (48.7519, -122.4787),
    "Yakima, WA": (46.6021, -120.5059),
    
    # Miami area stations
    "Tampa, FL": (27.9506, -82.4572),
    "Orlando, FL": (28.5383, -81.3792),
    "Jacksonville, FL": (30.3322, -81.6557),
    "Fort Lauderdale, FL": (26.1224, -80.1373),
    
    # Indianapolis area stations
    "Fort Wayne, IN": (41.0793, -85.1394),
    "Evansville, IN": (37.9716, -87.5711),
    "South Bend, IN": (41.6764, -86.2520),
    
    # Kansas City area stations
    "Topeka, KS": (39.0473, -95.6890),
    "Springfield, MO": (37.2153, -93.2982),
    "Omaha, NE": (41.2524, -95.9980),
    
    # Charlotte area stations
    "Greensboro, NC": (36.0726, -79.7920),
    "Asheville, NC": (35.5951, -82.5515),
    "Greenville, SC": (34.8526, -82.3940),
    
    # Additional regional stations
    "Boise, ID": (43.6150, -116.2023),
    "Albuquerque, NM": (35.0844, -106.6504),
    "Richmond, VA": (37.5407, -77.4360),
}

def calculate_distance(coord1, coord2):
    """Calculate distance between two coordinates using Haversine formula"""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in miles
    r = 3956
    return c * r

def get_closest_facilities(source_location, alternative_facilities, max_count=3):
    """Get the closest facilities to a source location"""
    if source_location not in CITY_COORDINATES:
        # Fallback to original behavior if coordinates not found
        return alternative_facilities[:max_count]
    
    source_coords = CITY_COORDINATES[source_location]
    facilities_with_distance = []
    
    for facility in alternative_facilities:
        # Handle both dict and sqlite3.Row objects
        if hasattr(facility, 'get'):
            facility_location = facility.get("location", "")
            current_load = facility.get("current_load", 0)
            max_capacity = facility.get("max_capacity", 1)
        else:
            facility_location = facility["location"] if "location" in facility else ""
            current_load = facility["current_load"] if "current_load" in facility else 0
            max_capacity = facility["max_capacity"] if "max_capacity" in facility else 1
            
        if facility_location in CITY_COORDINATES:
            distance = calculate_distance(source_coords, CITY_COORDINATES[facility_location])
            facilities_with_distance.append((facility, distance))
        else:
            # If coordinates not found, add with high distance (low priority)
            facilities_with_distance.append((facility, 9999))
    
    # Sort by distance first, then by capacity utilization
    facilities_with_distance.sort(key=lambda x: (
        x[1], 
        (x[0]["current_load"] if "current_load" in x[0] else 0) / (x[0]["max_capacity"] if "max_capacity" in x[0] else 1)
    ))
    
    return [facility for facility, distance in facilities_with_distance[:max_count]]


class RecommendationEngine:
    """AI-powered recommendation engine (simulated)"""

    @staticmethod
    def generate_recommendations() -> List[dict]:
        """Generate routing and operational recommendations"""
        from database import MetricsDB, FacilityDB

        recommendations = []

        # Get all facilities to check for staffing issues
        all_facilities = FacilityDB.get_all_active_facilities()
        
        # Check for low staffing and suggest temp agencies
        for facility in all_facilities:
            if facility['staffing_level'] is not None:
                facility_type = facility['facility_type']
                current_staff = facility['staffing_level']
                
                # Define minimum staffing thresholds
                if facility_type == 'hub' and current_staff < 120:  # Low for hubs (normal 100-300)
                    recommendations.append({
                        "type": "staffing_shortage",
                        "priority": "high" if current_staff < 100 else "medium",
                        "source_facility": facility['name'],
                        "facility_type": "Hub",
                        "reason": f"Hub staffing critically low at {current_staff} people (recommended minimum: 120)",
                        "suggested_action": "Contact temp agencies: Manpower, Adecco, or local staffing partners for warehouse/logistics workers",
                        "estimated_impact": f"Increase staffing to 150-200 people to improve productivity",
                    })
                elif facility_type == 'station' and current_staff < 15:  # Low for stations (normal 10-30)
                    recommendations.append({
                        "type": "staffing_shortage", 
                        "priority": "medium",
                        "source_facility": facility['name'],
                        "facility_type": "Station",
                        "reason": f"Station staffing low at {current_staff} people (recommended minimum: 15)",
                        "suggested_action": "Contract temp agency for delivery drivers and package handlers",
                        "estimated_impact": f"Increase to 18-22 staff to maintain delivery timeliness",
                    })

        # Get facilities with issues
        problem_facilities = MetricsDB.get_recent_problem_facilities()

        for facility in problem_facilities:
            # Find alternative facilities
            alternatives = FacilityDB.get_all_active_facilities()

            # Filter out current facility and find ones with capacity
            suitable_alternatives = [
                f
                for f in alternatives
                if f["id"] != facility["id"]
                and f["current_load"] < f["max_capacity"] * 0.8
            ]

            if suitable_alternatives:
                # Get closest facilities based on geographical proximity
                closest_facilities = get_closest_facilities(
                    facility["location"], suitable_alternatives, max_count=3
                )

                recommendations.append(
                    {
                        "type": "reroute",
                        "priority": "high"
                        if facility["equipment_status"] == "Down"
                        else "medium",
                        "source_facility": facility["name"],
                        "reason": f"Facility experiencing {facility['equipment_status']} with {facility['productivity_rate']:.1%} productivity",
                        "suggested_alternatives": [
                            alt["name"] for alt in closest_facilities
                        ],
                        "estimated_impact": f"Reduce load on {facility['name']} by 20-40%",
                    }
                )

        # Add weather-based recommendations with specific alternatives
        weather_locations = {
            "Chicago": {
                "highways": ["Use I-80 west to I-76 through Ohio", "Reroute via I-65 south to I-70"],
                "facilities": ["Milwaukee", "Indianapolis", "Cincinnati"]
            },
            "Denver": {
                "highways": ["Use I-70 through Kansas", "Reroute via I-25 south to I-40"],
                "facilities": ["Colorado Springs", "Kansas City", "Albuquerque"]
            },
            "Atlanta": {
                "highways": ["Use I-20 west route", "Reroute via I-77 through Carolinas"],
                "facilities": ["Nashville", "Charlotte", "Birmingham"]
            }
        }
        
        for location, alternatives in weather_locations.items():
            weather = DataService.get_weather_with_fallback(location)
            if weather and weather.alerts:
                # Create highway and facility suggestions
                highway_options = alternatives["highways"][:2]  # Limit to 2 options
                facility_options = alternatives["facilities"][:2]
                
                action_parts = []
                if highway_options:
                    action_parts.append(f"Highway alternatives: {', '.join(highway_options)}")
                if facility_options:
                    action_parts.append(f"Offload to nearby facilities: {', '.join(facility_options)}")
                
                recommendations.append(
                    {
                        "type": "weather_advisory",
                        "priority": "high" if "Storm" in weather.conditions or "Snow" in weather.conditions else "medium",
                        "location": location,
                        "source_facility": f"{location} Area",
                        "facility_type": "Region",
                        "reason": f"Weather alert: {', '.join(weather.alerts)}",
                        "suggested_action": "; ".join(action_parts),
                        "estimated_impact": "Prevent weather-related delays and maintain service levels",
                    }
                )

        # Add highway closure-based recommendations
        for i in range(1, 6):
            traffic = DataService.get_traffic_with_fallback(f"route-{i}")
            if traffic and traffic.estimated_delay_minutes > 30:
                rec_type = (
                    "highway_closure"
                    if "CLOSURE" in str(traffic.incidents)
                    else "highway_incident"
                )
                priority = "high" if traffic.estimated_delay_minutes > 120 else "medium"

                recommendations.append(
                    {
                        "type": rec_type,
                        "priority": priority,
                        "location": traffic.route_id,
                        "reason": f"Highway issue: {', '.join(traffic.incidents)} (Delay: {traffic.estimated_delay_minutes} min)",
                        "suggested_action": f"Use alternatives: {', '.join(traffic.alternative_routes[:2])}",
                        "estimated_impact": f"Avoid {traffic.estimated_delay_minutes} minute delays",
                    }
                )

        return recommendations
