# background_services.py - Background Data Collection Services
import threading
import time
from database import FacilityDB, MetricsDB, AlertsDB
from external_apis import DataService

class DataAggregator:
    """Background service that collects and stores real-time data"""
    
    def __init__(self):
        self.running = False
        self.thread = None
        self.collection_interval = 60  # seconds
    
    def start(self):
        """Start the data collection service"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._collect_data_loop, daemon=True)
            self.thread.start()
            print("Data aggregator started - collecting metrics every 60 seconds")
    
    def stop(self):
        """Stop the data collection service"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
            print("Data aggregator stopped")
    
    def _collect_data_loop(self):
        """Main data collection loop"""
        while self.running:
            try:
                print("Collecting facility metrics...")
                self._collect_facility_metrics()
                
                print("Checking for alerts...")
                self._check_for_alerts()
                
                print(f"Data collection complete. Next collection in {self.collection_interval} seconds.")
                time.sleep(self.collection_interval)
                
            except Exception as e:
                print(f"Error in data collection: {e}")
                time.sleep(10)  # Wait before retrying
    
    def _collect_facility_metrics(self):
        """Collect metrics for all active facilities"""
        facilities = FacilityDB.get_all_active_facilities()
        
        for facility in facilities:
            try:
                metrics = DataService.get_facility_metrics(facility['id'])
                if metrics:
                    MetricsDB.insert_metrics(metrics)
                    print(f"Collected metrics for {facility['name']}: "
                          f"Productivity {metrics.productivity_rate:.1%}, "
                          f"Equipment {metrics.equipment_status}")
                else:
                    print(f"No metrics available for {facility['name']}")
            except Exception as e:
                print(f"Error collecting metrics for facility {facility['id']}: {e}")
    
    def _check_for_alerts(self):
        """Check for conditions that warrant alerts"""
        try:
            # Check for facilities with low productivity
            self._check_productivity_alerts()
            
            # Check for equipment down
            self._check_equipment_alerts()
            
            # Check for high capacity utilization
            self._check_capacity_alerts()
            
        except Exception as e:
            print(f"Error checking alerts: {e}")
    
    def _check_productivity_alerts(self):
        """Check for low productivity alerts"""
        facilities = FacilityDB.get_all_active_facilities()
        
        for facility in facilities:
            if (facility['productivity_rate'] is not None and 
                facility['productivity_rate'] < 0.7):
                
                # Check if alert already exists
                if not AlertsDB.check_existing_alert(facility['id'], 'low_productivity'):
                    AlertsDB.insert_alert(
                        facility['id'], 
                        'low_productivity',
                        f"Facility {facility['name']} productivity at {facility['productivity_rate']:.1%}",
                        'warning'
                    )
                    print(f"ALERT: Low productivity at {facility['name']}")
    
    def _check_equipment_alerts(self):
        """Check for equipment down alerts"""
        facilities = FacilityDB.get_all_active_facilities()
        
        for facility in facilities:
            if facility['equipment_status'] == 'Down':
                # Check if alert already exists
                if not AlertsDB.check_existing_alert(facility['id'], 'equipment_down'):
                    AlertsDB.insert_alert(
                        facility['id'],
                        'equipment_down',
                        f"Equipment down at {facility['name']}",
                        'critical'
                    )
                    print(f"CRITICAL ALERT: Equipment down at {facility['name']}")
            
            elif facility['equipment_status'] == 'Maintenance':
                # Check if alert already exists
                if not AlertsDB.check_existing_alert(facility['id'], 'equipment_maintenance'):
                    AlertsDB.insert_alert(
                        facility['id'],
                        'equipment_maintenance',
                        f"Equipment under maintenance at {facility['name']}",
                        'warning'
                    )
                    print(f"WARNING: Equipment maintenance at {facility['name']}")
    
    def _check_capacity_alerts(self):
        """Check for high capacity utilization alerts"""
        facilities = FacilityDB.get_all_active_facilities()
        
        for facility in facilities:
            if facility['max_capacity'] > 0:
                utilization = facility['current_load'] / facility['max_capacity']
                
                if utilization > 0.9:  # Over 90% capacity
                    if not AlertsDB.check_existing_alert(facility['id'], 'high_capacity'):
                        AlertsDB.insert_alert(
                            facility['id'],
                            'high_capacity',
                            f"Facility {facility['name']} at {utilization:.1%} capacity",
                            'warning'
                        )
                        print(f"WARNING: High capacity utilization at {facility['name']}")

class SystemMonitor:
    """Monitor system health and performance"""
    
    def __init__(self):
        self.running = False
        self.thread = None
        self.monitor_interval = 300  # 5 minutes
    
    def start(self):
        """Start system monitoring"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.thread.start()
            print("System monitor started")
    
    def stop(self):
        """Stop system monitoring"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
            print("System monitor stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                self._check_api_health()
                self._check_database_health()
                time.sleep(self.monitor_interval)
            except Exception as e:
                print(f"Error in system monitoring: {e}")
                time.sleep(30)
    
    def _check_api_health(self):
        """Check health of external APIs"""
        # Test weather API
        weather_test = DataService.get_weather_with_fallback("Test")
        if weather_test is None:
            print("WARNING: Weather API services experiencing issues")
        
        # Test traffic API  
        traffic_test = DataService.get_traffic_with_fallback("test-route")
        if traffic_test is None:
            print("WARNING: Traffic API services experiencing issues")
    
    def _check_database_health(self):
        """Check database connectivity and performance"""
        try:
            facilities = FacilityDB.get_all_active_facilities()
            if len(facilities) == 0:
                print("WARNING: No active facilities found in database")
        except Exception as e:
            print(f"ERROR: Database health check failed: {e}")

# Global instances
data_aggregator = DataAggregator()
system_monitor = SystemMonitor()

def start_all_services():
    """Start all background services"""
    data_aggregator.start()
    system_monitor.start()

def stop_all_services():
    """Stop all background services"""
    data_aggregator.stop()
    system_monitor.stop()
