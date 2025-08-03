# background_services.py - Background Data Collection Services
import threading
import time
from database import FacilityDB, MetricsDB, AlertsDB
from .external_apis import DataService

class DataAggregator:
    """Background service that collects and stores real-time data"""
    
    def __init__(self):
        self.running = False
        self.thread = None
        self.collection_interval = 600  # 10 minutes - reduced frequency to minimize db contention
    
    def start(self):
        """Start the data collection service"""
        if not self.running:
            self.running = True
            # Sync alerts on startup to fix any inconsistencies
            self.sync_alerts_with_current_data()
            self.thread = threading.Thread(target=self._collect_data_loop, daemon=True)
            self.thread.start()
            print("Data aggregator started - collecting metrics every 10 minutes")
    
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
                self._collect_facility_metrics()
                self._check_for_alerts()
                time.sleep(self.collection_interval)
                
            except Exception as e:
                print(f"Error in data collection: {e}")
                time.sleep(10)  # Wait before retrying
    
    def _collect_facility_metrics(self):
        """Collect metrics for all active facilities using batch operations"""
        facilities = FacilityDB.get_all_active_facilities()
        metrics_batch = []
        
        # Collect all metrics first
        for facility in facilities:
            try:
                metrics = DataService.get_facility_metrics(facility['id'], facility['facility_type'])
                if metrics:
                    metrics_batch.append(metrics)
            except Exception as e:
                print(f"Error collecting metrics for facility {facility['id']}: {e}")
        
        # Batch insert all metrics in a single transaction
        if metrics_batch:
            try:
                self._batch_insert_metrics(metrics_batch)
            except Exception as e:
                print(f"Error batch inserting metrics: {e}")
                # Fallback to individual inserts
                for metrics in metrics_batch:
                    try:
                        MetricsDB.insert_metrics(metrics)
                    except Exception as e2:
                        print(f"Error inserting metrics for facility {metrics.facility_id}: {e2}")
    
    def _batch_insert_metrics(self, metrics_list):
        """Insert multiple metrics in a single transaction"""
        from database import get_db_connection, retry_db_operation, INSERT_FACILITY_METRICS
        
        def _batch_insert():
            conn = get_db_connection()
            try:
                for metrics in metrics_list:
                    conn.execute(INSERT_FACILITY_METRICS, 
                                (metrics.facility_id, metrics.staffing_level, metrics.productivity_rate, 
                                 metrics.equipment_status, metrics.downtime_minutes, metrics.delivery_timeliness))
                conn.commit()
            finally:
                conn.close()
        
        retry_db_operation(_batch_insert)
    
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
    
    def _check_equipment_alerts(self):
        """Check for equipment down alerts with improved consistency"""
        facilities = FacilityDB.get_all_active_facilities()
        
        for facility in facilities:
            facility_id = facility['id']
            facility_name = facility['name']
            equipment_status = facility['equipment_status']
            
            if equipment_status == 'Down':
                # Check if alert already exists
                if not AlertsDB.check_existing_alert(facility_id, 'equipment_down'):
                    AlertsDB.insert_alert(
                        facility_id,
                        'equipment_down',
                        f"Equipment down at {facility_name}",
                        'critical'
                    )
            
            elif equipment_status == 'Maintenance':
                # Check if alert already exists
                if not AlertsDB.check_existing_alert(facility_id, 'equipment_maintenance'):
                    AlertsDB.insert_alert(
                        facility_id,
                        'equipment_maintenance',
                        f"Equipment under maintenance at {facility_name}",
                        'warning'
                    )
            
            else:
                # If equipment is now operational, resolve existing alerts
                if equipment_status == 'Operational':
                    self._resolve_equipment_alerts_for_facility(facility_id)
    
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
    
    def _resolve_equipment_alerts_for_facility(self, facility_id):
        """Resolve equipment-related alerts when equipment becomes operational"""
        try:
            from database import get_db_connection
            conn = get_db_connection()
            
            # Resolve equipment_down and equipment_maintenance alerts for this facility
            conn.execute("""
                UPDATE alerts 
                SET resolved = TRUE 
                WHERE facility_id = ? 
                AND alert_type IN ('equipment_down', 'equipment_maintenance') 
                AND resolved = FALSE
            """, (facility_id,))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error resolving equipment alerts for facility {facility_id}: {e}")
    
    def sync_alerts_with_current_data(self):
        """Synchronize alerts with current facility data to fix inconsistencies"""
        try:
            print("Synchronizing alerts with current facility data...")
            facilities = FacilityDB.get_all_active_facilities()
            
            for facility in facilities:
                facility_id = facility['id']
                facility_name = facility['name']
                equipment_status = facility['equipment_status']
                
                if equipment_status == 'Down':
                    # Ensure there's an equipment_down alert
                    if not AlertsDB.check_existing_alert(facility_id, 'equipment_down'):
                        AlertsDB.insert_alert(
                            facility_id,
                            'equipment_down',
                            f"Equipment down at {facility_name}",
                            'critical'
                        )
                
                elif equipment_status == 'Maintenance':
                    # Ensure there's an equipment_maintenance alert
                    if not AlertsDB.check_existing_alert(facility_id, 'equipment_maintenance'):
                        AlertsDB.insert_alert(
                            facility_id,
                            'equipment_maintenance',
                            f"Equipment under maintenance at {facility_name}",
                            'warning'
                        )
                
                elif equipment_status == 'Operational':
                    # Resolve any existing equipment alerts
                    self._resolve_equipment_alerts_for_facility(facility_id)
                
                # Check productivity alerts
                if (facility['productivity_rate'] is not None and 
                    facility['productivity_rate'] < 0.7):
                    if not AlertsDB.check_existing_alert(facility_id, 'low_productivity'):
                        AlertsDB.insert_alert(
                            facility_id, 
                            'low_productivity',
                            f"Facility {facility_name} productivity at {facility['productivity_rate']:.1%}",
                            'warning'
                        )
            
            print("Alert synchronization completed.")
            
        except Exception as e:
            print(f"Error during alert synchronization: {e}")

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
