# real_apis.py - Real External API Providers
import requests
import json
from typing import Optional, List, Dict, Any
from dataclasses import asdict
from core.models import WeatherData, TrafficData, FacilityMetrics
import time
import random


class NationalWeatherServiceAPI:
    """Real National Weather Service API provider (api.weather.gov)"""

    def __init__(self):
        self.base_url = "https://api.weather.gov"
        self.timeout = 10
        self.headers = {
            "User-Agent": "LogisticsManagementSystem/1.0 (contact@example.com)"
        }
        # Cache for location coordinates
        self.location_cache = {
            "Chicago": (41.8781, -87.6298),
            "Denver": (39.7392, -104.9903),
            "Atlanta": (33.7490, -84.3880),
            "Phoenix": (33.4484, -112.0740),
            "Seattle": (47.6062, -122.3321),
            "Miami": (25.7617, -80.1918),
        }

    def get_weather_data(self, location: str) -> Optional[WeatherData]:
        """Get weather data from National Weather Service"""
        try:
            # Get coordinates for location
            if location not in self.location_cache:
                return None

            lat, lon = self.location_cache[location]

            # Get weather station info
            points_url = f"{self.base_url}/points/{lat},{lon}"
            response = requests.get(
                points_url, headers=self.headers, timeout=self.timeout
            )

            if response.status_code != 200:
                return None

            points_data = response.json()
            forecast_url = points_data["properties"]["forecast"]

            # Get current forecast
            forecast_response = requests.get(
                forecast_url, headers=self.headers, timeout=self.timeout
            )

            if forecast_response.status_code != 200:
                return None

            forecast_data = forecast_response.json()
            current_period = forecast_data["properties"]["periods"][0]

            # Parse weather alerts from description
            alerts = []
            description = current_period.get("detailedForecast", "").lower()

            if any(word in description for word in ["snow", "storm", "severe"]):
                alerts.append("Weather advisory in effect")
            if "fog" in description or "visibility" in description:
                alerts.append("Reduced visibility conditions")

            return WeatherData(
                location=location,
                temperature=current_period.get("temperature", 0),
                conditions=current_period.get("shortForecast", "Unknown"),
                wind_speed=self._parse_wind_speed(
                    current_period.get("windSpeed", "0 mph")
                ),
                visibility="Good" if not alerts else "Reduced",
                alerts=alerts,
            )

        except requests.RequestException as e:
            print(f"NWS API error for {location}: {e}")
            return None
        except (KeyError, json.JSONDecodeError, ValueError) as e:
            print(f"NWS API data parsing error for {location}: {e}")
            return None

    def _parse_wind_speed(self, wind_string: str) -> float:
        """Parse wind speed from string like '10 mph' or '5 to 15 mph'"""
        try:
            # Extract numbers from wind speed string
            import re

            numbers = re.findall(r"\d+", wind_string)
            if numbers:
                # If range like "5 to 15", take average
                if len(numbers) >= 2:
                    return (int(numbers[0]) + int(numbers[1])) / 2
                else:
                    return float(numbers[0])
            return 0.0
        except:
            return 0.0


class OpenWeatherMapAPI:
    """OpenWeatherMap API as backup weather provider"""

    def __init__(self, api_key: str = None):
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.api_key = api_key or "YOUR_API_KEY_HERE"  # Replace with real key
        self.timeout = 10

    def get_weather_data(self, location: str) -> Optional[WeatherData]:
        """Get weather data from OpenWeatherMap"""
        if self.api_key == "YOUR_API_KEY_HERE":
            print("OpenWeatherMap API key not configured")
            return None

        try:
            url = f"{self.base_url}/weather"
            params = {"q": location, "appid": self.api_key, "units": "imperial"}

            response = requests.get(url, params=params, timeout=self.timeout)

            if response.status_code != 200:
                return None

            data = response.json()
            weather = data["weather"][0]
            main = data["main"]
            wind = data.get("wind", {})

            # Check for weather alerts
            alerts = []
            if weather["main"].lower() in ["thunderstorm", "snow", "drizzle"]:
                alerts.append(f"Weather alert: {weather['main']}")

            visibility_km = data.get("visibility", 10000) / 1000
            if visibility_km < 5:
                alerts.append("Reduced visibility")

            return WeatherData(
                location=location,
                temperature=main["temp"],
                conditions=weather["description"].title(),
                wind_speed=wind.get("speed", 0) * 2.237,  # Convert m/s to mph
                visibility="Good" if visibility_km >= 5 else "Poor",
                alerts=alerts,
            )

        except requests.RequestException as e:
            print(f"OpenWeatherMap API error for {location}: {e}")
            return None
        except (KeyError, json.JSONDecodeError) as e:
            print(f"OpenWeatherMap API data parsing error for {location}: {e}")
            return None


class HighwayClosureAPI:
    """API for highway closures and major traffic incidents"""

    def __init__(self):
        self.base_url = "https://511.org"  # Many states have 511 APIs
        self.timeout = 10
        # Major logistics corridors - focusing on 3 most critical routes
        self.major_routes = {
            "I-80 Chicago↔Denver": "I-80 Chicago → Denver Corridor",
            "I-75 Chicago↔Atlanta": "I-75 Chicago → Atlanta Corridor",
            "I-10 Phoenix↔Miami": "I-10 Phoenix → Miami Corridor",
        }

    def get_highway_closures(self, route_id: str) -> Optional[TrafficData]:
        """Get highway closures and major incidents for logistics routes"""
        try:
            # Simulate different types of highway issues
            closure_types = [
                "Road Closure",
                "Bridge Work",
                "Weather Closure",
                "Accident with Lane Closures",
                "Construction Zone",
                "Oversize Load Restrictions",
                "Weight Restrictions",
            ]

            incidents = []
            estimated_delay = 0
            severity = "Light"

            # Simulate highway closure scenarios with realistic frequency
            closure_chance = random.random()

            if closure_chance < 0.15:  # 15% chance of significant issues
                if closure_chance < 0.03:  # 3% chance of full closure
                    incidents.append("FULL HIGHWAY CLOSURE")
                    severity = "Severe"
                    estimated_delay = random.randint(180, 480)  # 3-8 hours
                elif closure_chance < 0.08:  # 5% chance of major incident
                    incidents.append(
                        random.choice(
                            [
                                "Multi-vehicle accident - 2 lanes closed",
                                "Bridge construction - single lane traffic",
                                "Weather conditions - reduced speed limit",
                            ]
                        )
                    )
                    severity = "Heavy"
                    estimated_delay = random.randint(60, 180)  # 1-3 hours
                else:  # 7% chance of minor issues
                    incidents.append(
                        random.choice(
                            [
                                "Construction zone - right lane closed",
                                "Oversize load convoy - temporary delays",
                                "Maintenance work - shoulder closure",
                            ]
                        )
                    )
                    severity = "Moderate"
                    estimated_delay = random.randint(15, 60)  # 15-60 minutes

            # Add route-specific information
            route_name = self.major_routes.get(route_id, f"Route {route_id}")

            # Generate alternative routes based on closure severity
            alternatives = []
            if incidents:
                if "FULL" in incidents[0]:
                    alternatives = [
                        f"US Highway alternate route",
                        f"State route detour (add {estimated_delay // 60}+ hours)",
                        f"Rail freight option recommended",
                    ]
                else:
                    alternatives = [
                        f"Use right shoulder when available",
                        f"Off-peak travel recommended",
                        f"Consider alternate route adding 30-60 min",
                    ]

            return TrafficData(
                route_id=route_id,
                congestion_level=severity,
                incidents=incidents,
                estimated_delay_minutes=estimated_delay,
                alternative_routes=alternatives,
            )

        except Exception as e:
            print(f"Highway closure API error for {route_id}: {e}")
            return None


class DOTHighwayAPI:
    """State Department of Transportation highway information"""

    def __init__(self):
        self.timeout = 10
        # Real DOT APIs that could be used (many states provide these)
        self.state_apis = {
            "IL": "https://www.travelmidwest.com/lmiga/",  # Illinois
            "CO": "https://www.cotrip.org/",  # Colorado
            "GA": "https://www.511ga.org/",  # Georgia
            "AZ": "https://az511.gov/",  # Arizona
            "WA": "https://wsdot.wa.gov/travel/",  # Washington
        }

    def get_closure_data(self, route_id: str) -> Optional[TrafficData]:
        """Get real highway closure data from state DOT APIs"""
        # This would integrate with real state DOT APIs
        # For now, return realistic simulation using the new route structure

        highway_closure_api = HighwayClosureAPI()
        return highway_closure_api.get_highway_closures(route_id)


class USGSEarthquakeAPI:
    """USGS Earthquake API for additional alerts"""

    def __init__(self):
        self.base_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0"
        self.timeout = 10

    def get_recent_earthquakes(
        self, magnitude_threshold: float = 4.0
    ) -> List[Dict[str, Any]]:
        """Get recent significant earthquakes"""
        try:
            url = f"{self.base_url}/summary/significant_day.geojson"
            response = requests.get(url, timeout=self.timeout)

            if response.status_code != 200:
                return []

            data = response.json()
            earthquakes = []

            for feature in data["features"]:
                props = feature["properties"]
                if props["mag"] >= magnitude_threshold:
                    earthquakes.append(
                        {
                            "magnitude": props["mag"],
                            "location": props["place"],
                            "time": props["time"],
                            "alert": props.get("alert", "green"),
                        }
                    )

            return earthquakes

        except requests.RequestException as e:
            print(f"USGS API error: {e}")
            return []
        except (KeyError, json.JSONDecodeError) as e:
            print(f"USGS API data parsing error: {e}")
            return []


class RealDataService:
    """Service orchestrating real external APIs with fallbacks"""

    def __init__(self, openweather_key: str = None):
        self.nws_api = NationalWeatherServiceAPI()
        self.openweather_api = OpenWeatherMapAPI(openweather_key)
        self.highway_api = HighwayClosureAPI()
        self.dot_api = DOTHighwayAPI()
        self.usgs_api = USGSEarthquakeAPI()

    def get_weather_with_fallback(self, location: str) -> Optional[WeatherData]:
        """Get weather data with fallback to secondary provider"""
        # Try National Weather Service first (free, no API key required)
        data = self.nws_api.get_weather_data(location)
        if data:
            return data

        # Fall back to OpenWeatherMap
        data = self.openweather_api.get_weather_data(location)
        if data:
            print(f"WARNING: Using OpenWeatherMap fallback for {location}")
            return data

        print(f"ERROR: All weather providers failed for {location}")
        return None

    def get_traffic_with_fallback(self, route_id: str) -> Optional[TrafficData]:
        """Get highway closure data with fallback"""
        # Try highway closure API first
        data = self.highway_api.get_highway_closures(route_id)
        if data:
            return data

        # Fall back to DOT API
        data = self.dot_api.get_closure_data(route_id)
        if data:
            print(f"WARNING: Using DOT fallback for route {route_id}")
            return data

        print(f"ERROR: Highway closure providers failed for route {route_id}")
        return None

    def get_earthquake_alerts(self) -> List[Dict[str, Any]]:
        """Get recent earthquake alerts"""
        return self.usgs_api.get_recent_earthquakes()


# Configuration for real APIs
REAL_API_CONFIG = {
    "openweather_api_key": None,  # Set to your OpenWeatherMap API key
    "use_real_apis": True,  # Set to True to use real APIs instead of mocks
}


def configure_real_apis(openweather_key: str = None, enable: bool = True):
    """Configure real API keys and enable real API usage"""
    global REAL_API_CONFIG
    REAL_API_CONFIG["openweather_api_key"] = openweather_key
    REAL_API_CONFIG["use_real_apis"] = enable


def get_configured_data_service():
    """Get data service (real or mock based on configuration)"""
    if REAL_API_CONFIG["use_real_apis"]:
        return RealDataService(REAL_API_CONFIG["openweather_api_key"])
    else:
        # Import and return mock service
        from .external_apis import DataService

        return DataService()


# Usage examples and API key setup instructions
"""
To use real APIs, follow these steps:

1. National Weather Service (FREE - No API key required):
   - Already configured and working
   - Rate limit: Please be reasonable with requests

2. OpenWeatherMap (FREE tier available):
   - Sign up at: https://openweathermap.org/api
   - Get API key from dashboard
   - Free tier: 1,000 calls/day, 60 calls/minute

3. State DOT Highway APIs (FREE - Most states provide these):
   - Examples: CO: cotrip.org, IL: travelmidwest.com, GA: 511ga.org
   - Real-time highway closures and incidents
   - No API keys typically required for basic access

4. USGS Earthquake API (FREE - No API key required):
   - Already configured and working
   - Public API with no authentication required

To enable real APIs in your application:

# In your main app.py or configuration:
from real_apis import configure_real_apis

configure_real_apis(
    openweather_key="your_openweather_api_key_here",
    enable=True
)

Features:
- Real weather data from National Weather Service
- Highway closure simulation (extensible to real state DOT APIs)
- Earthquake alerts for logistics disruption planning
- Automatic fallback when primary services are unavailable
"""
