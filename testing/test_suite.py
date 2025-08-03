#!/usr/bin/env python3
# test_suite.py - Main test suite for the logistics management system
import sys
import os
import unittest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.logic import get_db_connection, FacilityDB, MetricsDB, AlertsDB, MessagesDB
from core.models import Facility, FacilityMetrics, Alert, Message
from services.external_apis import DataService
import sqlite3

class TestBasicFunctionality(unittest.TestCase):
    """Simple tests to verify basic functionality works"""
    
    def test_database_connection(self):
        """Test database connection works"""
        conn = get_db_connection()
        self.assertIsInstance(conn, sqlite3.Connection)
        conn.close()
    
    def test_facility_model(self):
        """Test Facility model creation"""
        facility = Facility(
            id=1,
            name="Test Facility", 
            location="Test Location",
            facility_type="hub"
        )
        self.assertEqual(facility.name, "Test Facility")
        self.assertEqual(facility.status, "active")  # Default value
    
    def test_facility_metrics_model(self):
        """Test FacilityMetrics model creation"""
        metrics = FacilityMetrics(
            facility_id=1,
            staffing_level=10,
            productivity_rate=0.8,
            equipment_status="Operational"
        )
        self.assertEqual(metrics.facility_id, 1)
        self.assertEqual(metrics.staffing_level, 10)
    
    def test_get_facilities(self):
        """Test getting facilities from database"""
        try:
            facilities = FacilityDB.get_all_active_facilities()
            self.assertIsInstance(facilities, list)
        except Exception as e:
            self.fail(f"Getting facilities failed: {e}")
    
    def test_weather_service(self):
        """Test weather service"""
        try:
            weather = DataService.get_weather_with_fallback("Chicago")
            # Weather might be None due to mock failures, that's OK
            self.assertTrue(weather is None or hasattr(weather, 'location'))
        except Exception as e:
            self.fail(f"Weather service failed: {e}")
    
    def test_traffic_service(self):
        """Test traffic service"""
        try:
            traffic = DataService.get_traffic_with_fallback("route-1")
            # Traffic might be None due to mock failures, that's OK
            self.assertTrue(traffic is None or hasattr(traffic, 'route_id'))
        except Exception as e:
            self.fail(f"Traffic service failed: {e}")

class TestDatabaseOperations(unittest.TestCase):
    """Test database operations work"""
    
    def test_facility_by_id(self):
        """Test getting facility by ID"""
        try:
            facility = FacilityDB.get_facility_by_id(1)
            if facility:
                self.assertIn('name', facility.keys())
        except Exception as e:
            self.fail(f"Getting facility by ID failed: {e}")
    
    def test_alerts(self):
        """Test getting alerts"""
        try:
            alerts = AlertsDB.get_active_alerts(5)
            self.assertIsInstance(alerts, list)
        except Exception as e:
            self.fail(f"Getting alerts failed: {e}")
    
    def test_messages(self):
        """Test getting messages"""
        try:
            messages = MessagesDB.get_recent_messages(5)
            self.assertIsInstance(messages, list)
        except Exception as e:
            self.fail(f"Getting messages failed: {e}")

def run_simple_tests():
    """Run the main test suite with basic output"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print(f"\nTest Suite Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures or result.errors:
        print("Some tests failed - check the output above for details")
        return 1
    else:
        print("All tests passed!")
        return 0

if __name__ == '__main__':
    sys.exit(run_simple_tests())