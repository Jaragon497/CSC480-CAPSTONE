# external_apis.py - External API Providers with Fallback
import random
from typing import Optional, List
from dataclasses import asdict
from models import WeatherData, TrafficData, FacilityMetrics


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
            "I-80-Chicago-Denver": "I-80 Chicago → Denver Corridor",
            "I-75-Chicago-Atlanta": "I-75 Chicago → Atlanta Corridor",
            "I-10-Phoenix-Miami": "I-10 Phoenix → Miami Corridor",
        }

    def get_traffic_data(self, route_id: str) -> Optional[TrafficData]:
        """Get highway closure and incident data"""
        # Simulate API failure
        if random.random() < self.failure_rate:
            return None

        # Highway closure scenarios with route-specific incidents
        route_specific_incidents = {
            "I-80-Chicago-Denver": [
                "Winter weather closure near Des Moines",
                "Bridge construction in Nebraska - single lane",
                "High wind restrictions for high-profile vehicles",
                "Oversize load convoy - 30 min delays",
            ],
            "I-75-Chicago-Atlanta": [
                "Construction in Kentucky - lane restrictions",
                "Fog conditions in Tennessee valleys",
                "Multi-vehicle accident near Cincinnati",
                "Road work in Georgia - expect delays",
            ],
            "I-10-Phoenix-Miami": [
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
            "I-80-Chicago-Denver": [
                "I-76 through Pennsylvania/Ohio (longer)",
                "I-70 through Kansas (southern route)",
                "Rail freight via BNSF recommended",
            ],
            "I-75-Chicago-Atlanta": [
                "I-65 through Alabama (western route)",
                "I-77 through West Virginia (eastern route)",
                "CSX rail service available",
            ],
            "I-10-Phoenix-Miami": [
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
    """Mock internal company data provider"""

    def __init__(self):
        self.failure_rate = 0.05  # 5% chance of data unavailability

    def get_facility_metrics(self, facility_id: int) -> Optional[FacilityMetrics]:
        """Get metrics for a facility"""
        # Simulate occasional data unavailability
        if random.random() < self.failure_rate:
            return None

        equipment_statuses = ["Operational", "Maintenance", "Down", "Reduced Capacity"]
        equipment_weights = [0.7, 0.15, 0.05, 0.1]

        return FacilityMetrics(
            facility_id=facility_id,
            staffing_level=random.randint(5, 25),
            productivity_rate=random.uniform(0.6, 1.2),
            equipment_status=random.choices(
                equipment_statuses, weights=equipment_weights
            )[0],
            downtime_minutes=random.randint(0, 60) if random.random() < 0.3 else 0,
        )


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
    def get_facility_metrics(facility_id: int) -> Optional[FacilityMetrics]:
        """Get facility metrics from internal provider"""
        return internal_data.get_facility_metrics(facility_id)


class RecommendationEngine:
    """AI-powered recommendation engine (simulated)"""

    @staticmethod
    def generate_recommendations() -> List[dict]:
        """Generate routing and operational recommendations"""
        from database import MetricsDB, FacilityDB

        recommendations = []

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
                # Sort by available capacity
                suitable_alternatives.sort(
                    key=lambda x: x["current_load"] / x["max_capacity"]
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
                            alt["name"] for alt in suitable_alternatives[:3]
                        ],
                        "estimated_impact": f"Reduce load on {facility['name']} by 20-40%",
                    }
                )

        # Add weather-based recommendations
        weather_locations = ["Chicago", "Denver", "Atlanta"]
        for location in weather_locations:
            weather = DataService.get_weather_with_fallback(location)
            if weather and weather.alerts:
                recommendations.append(
                    {
                        "type": "weather_advisory",
                        "priority": "medium",
                        "location": location,
                        "reason": f"Weather alert: {', '.join(weather.alerts)}",
                        "suggested_action": "Consider rerouting shipments away from affected area",
                        "estimated_impact": "Prevent weather-related delays",
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
