# logic.py - Database Operations and Management
import sqlite3
import time
import random
from typing import List, Optional, Dict, Any
from core.models import Facility, FacilityMetrics, Alert, Message, Route
from .sql_queries import *

DATABASE = 'logistics.db'

def get_db_connection():
    """Get database connection with row factory and timeout"""
    conn = sqlite3.connect(DATABASE, timeout=30.0)  # 30-second timeout
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for better concurrency
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA temp_store=memory")
    conn.execute("PRAGMA mmap_size=268435456")  # 256MB mmap
    return conn

def retry_db_operation(operation_func, max_retries=3, base_delay=0.1):
    """Retry database operations with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return operation_func()
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e).lower() and attempt < max_retries - 1:
                # Exponential backoff with jitter
                delay = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                time.sleep(delay)
                continue
            else:
                raise
        except Exception as e:
            # For non-locking errors, don't retry
            raise
    
def init_database():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    
    # Create all tables
    conn.execute(CREATE_FACILITIES_TABLE)
    conn.execute(CREATE_FACILITY_METRICS_TABLE)
    conn.execute(CREATE_MESSAGES_TABLE)
    conn.execute(CREATE_ROUTES_TABLE)
    conn.execute(CREATE_ALERTS_TABLE)
    
    conn.commit()
    conn.close()

class FacilityDB:
    """Database operations for facilities"""
    
    @staticmethod
    def get_all_active_facilities():
        """Get all active facilities with latest metrics"""
        conn = get_db_connection()
        facilities = conn.execute(GET_ALL_ACTIVE_FACILITIES_WITH_METRICS).fetchall()
        conn.close()
        return facilities
    
    @staticmethod
    def get_facility_by_id(facility_id: int):
        """Get facility by ID"""
        conn = get_db_connection()
        facility = conn.execute(GET_FACILITY_BY_ID, (facility_id,)).fetchone()
        conn.close()
        return facility
    
    @staticmethod
    def get_all_facilities():
        """Get all facilities (for dropdown lists)"""
        conn = get_db_connection()
        facilities = conn.execute(GET_ALL_ACTIVE_FACILITIES).fetchall()
        conn.close()
        return facilities

class MetricsDB:
    """Database operations for facility metrics"""
    
    @staticmethod
    def insert_metrics(metrics: FacilityMetrics):
        """Insert facility metrics with retry logic"""
        def _insert():
            conn = get_db_connection()
            try:
                conn.execute(INSERT_FACILITY_METRICS, 
                            (metrics.facility_id, metrics.staffing_level, metrics.productivity_rate, 
                             metrics.equipment_status, metrics.downtime_minutes, metrics.delivery_timeliness))
                conn.commit()
            finally:
                conn.close()
        
        retry_db_operation(_insert)
    
    @staticmethod
    def get_facility_metrics(facility_id: int, limit: int = 24) -> List[sqlite3.Row]:
        """Get recent metrics for a facility"""
        conn = get_db_connection()
        metrics = conn.execute(GET_FACILITY_METRICS, (facility_id, limit)).fetchall()
        conn.close()
        return metrics
    
    @staticmethod
    def get_recent_problem_facilities():
        """Get facilities with recent issues"""
        conn = get_db_connection()
        problem_facilities = conn.execute(GET_RECENT_PROBLEM_FACILITIES).fetchall()
        conn.close()
        return problem_facilities

class AlertsDB:
    """Database operations for alerts"""
    
    @staticmethod
    def get_active_alerts(limit: int = 10):
        """Get active alerts"""
        conn = get_db_connection()
        alerts = conn.execute(GET_ACTIVE_ALERTS, (limit,)).fetchall()
        conn.close()
        return alerts
    
    @staticmethod
    def get_facility_alerts(facility_id: int, limit: int = 10):
        """Get alerts for a specific facility"""
        conn = get_db_connection()
        alerts = conn.execute(GET_FACILITY_ALERTS, (facility_id, limit)).fetchall()
        conn.close()
        return alerts
    
    @staticmethod
    def insert_alert(facility_id: int, alert_type: str, message: str, severity: str = 'info'):
        """Insert new alert with retry logic"""
        def _insert():
            conn = get_db_connection()
            try:
                conn.execute(INSERT_ALERT, (facility_id, alert_type, message, severity))
                conn.commit()
            finally:
                conn.close()
        
        retry_db_operation(_insert)
    
    @staticmethod
    def resolve_alert(alert_id: int):
        """Mark alert as resolved"""
        conn = get_db_connection()
        conn.execute(RESOLVE_ALERT, (alert_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def check_existing_alert(facility_id: int, alert_type: str, hours: int = 1):
        """Check if similar alert already exists"""
        conn = get_db_connection()
        existing = conn.execute(CHECK_EXISTING_ALERT.format(hours), 
                               (facility_id, alert_type)).fetchone()
        conn.close()
        return existing is not None

class MessagesDB:
    """Database operations for messages"""
    
    @staticmethod
    def get_recent_messages(limit: int = 20):
        """Get recent messages"""
        conn = get_db_connection()
        messages = conn.execute(GET_RECENT_MESSAGES, (limit,)).fetchall()
        conn.close()
        return messages
    
    @staticmethod
    def insert_message(from_facility_id: int, to_facility_id: int, message: str, priority: str = 'normal'):
        """Insert new message"""
        conn = get_db_connection()
        conn.execute(INSERT_MESSAGE, (from_facility_id, to_facility_id, message, priority))
        conn.commit()
        conn.close()

def seed_sample_data():
    """Seed the database with comprehensive logistics network data"""
    from .network_data import get_all_facilities, get_all_routes
    
    conn = get_db_connection()
    
    # Check if data already exists
    existing = conn.execute(COUNT_FACILITIES).fetchone()
    if existing['count'] > 0:
        conn.close()
        return
    
    # Load comprehensive network data
    facilities = get_all_facilities()
    routes = get_all_routes()
    
    # Insert all facilities
    for facility in facilities:
        conn.execute(INSERT_FACILITY, facility)
    
    # Insert all routes
    for route in routes:
        conn.execute(INSERT_ROUTE, route)
    
    conn.commit()
    conn.close()
    print(f"Database initialized: {len(facilities)} facilities, {len(routes)} routes")