# database.py - Database Operations and Management
import sqlite3
from typing import List, Optional, Dict, Any
from models import Facility, FacilityMetrics, Alert, Message, Route

DATABASE = 'logistics.db'

def get_db_connection():
    """Get database connection with row factory"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    
    # Facilities table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS facilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            facility_type TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            max_capacity INTEGER DEFAULT 1000,
            current_load INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Real-time metrics table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS facility_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facility_id INTEGER,
            staffing_level INTEGER,
            productivity_rate REAL,
            equipment_status TEXT,
            downtime_minutes INTEGER DEFAULT 0,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (facility_id) REFERENCES facilities (id)
        )
    ''')
    
    # Messages table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_facility_id INTEGER,
            to_facility_id INTEGER,
            message TEXT NOT NULL,
            priority TEXT DEFAULT 'normal',
            status TEXT DEFAULT 'sent',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (from_facility_id) REFERENCES facilities (id),
            FOREIGN KEY (to_facility_id) REFERENCES facilities (id)
        )
    ''')
    
    # Routes table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_facility_id INTEGER,
            to_facility_id INTEGER,
            distance_miles INTEGER,
            estimated_time_hours REAL,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (from_facility_id) REFERENCES facilities (id),
            FOREIGN KEY (to_facility_id) REFERENCES facilities (id)
        )
    ''')
    
    # Alerts table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facility_id INTEGER,
            alert_type TEXT NOT NULL,
            message TEXT NOT NULL,
            severity TEXT DEFAULT 'info',
            resolved BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (facility_id) REFERENCES facilities (id)
        )
    ''')
    
    conn.commit()
    conn.close()

class FacilityDB:
    """Database operations for facilities"""
    
    @staticmethod
    def get_all_active_facilities():
        """Get all active facilities with latest metrics"""
        conn = get_db_connection()
        facilities = conn.execute('''
            SELECT f.*, 
                   fm.productivity_rate, 
                   fm.staffing_level, 
                   fm.equipment_status,
                   fm.timestamp as last_updated
            FROM facilities f
            LEFT JOIN facility_metrics fm ON f.id = fm.facility_id
            WHERE f.status = 'active'
            AND (fm.id IS NULL OR fm.id = (
                SELECT id FROM facility_metrics fm2 
                WHERE fm2.facility_id = f.id 
                ORDER BY timestamp DESC LIMIT 1
            ))
            ORDER BY f.name
        ''').fetchall()
        conn.close()
        return facilities
    
    @staticmethod
    def get_facility_by_id(facility_id: int):
        """Get facility by ID"""
        conn = get_db_connection()
        facility = conn.execute('SELECT * FROM facilities WHERE id = ?', (facility_id,)).fetchone()
        conn.close()
        return facility
    
    @staticmethod
    def get_all_facilities():
        """Get all facilities (for dropdown lists)"""
        conn = get_db_connection()
        facilities = conn.execute('SELECT * FROM facilities WHERE status = "active" ORDER BY name').fetchall()
        conn.close()
        return facilities

class MetricsDB:
    """Database operations for facility metrics"""
    
    @staticmethod
    def insert_metrics(metrics: FacilityMetrics):
        """Insert facility metrics"""
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO facility_metrics 
            (facility_id, staffing_level, productivity_rate, equipment_status, downtime_minutes)
            VALUES (?, ?, ?, ?, ?)
        ''', (metrics.facility_id, metrics.staffing_level, metrics.productivity_rate, 
              metrics.equipment_status, metrics.downtime_minutes))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_facility_metrics(facility_id: int, limit: int = 24) -> List[sqlite3.Row]:
        """Get recent metrics for a facility"""
        conn = get_db_connection()
        metrics = conn.execute('''
            SELECT * FROM facility_metrics 
            WHERE facility_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (facility_id, limit)).fetchall()
        conn.close()
        return metrics
    
    @staticmethod
    def get_recent_problem_facilities():
        """Get facilities with recent issues"""
        conn = get_db_connection()
        problem_facilities = conn.execute('''
            SELECT f.id, f.name, f.location, f.current_load, f.max_capacity,
                   fm.productivity_rate, fm.equipment_status, fm.staffing_level
            FROM facilities f
            JOIN facility_metrics fm ON f.id = fm.facility_id
            WHERE fm.timestamp > datetime('now', '-10 minutes')
            AND (fm.productivity_rate < 0.8 OR fm.equipment_status IN ('Down', 'Maintenance'))
            AND fm.id = (
                SELECT id FROM facility_metrics fm2 
                WHERE fm2.facility_id = f.id 
                ORDER BY timestamp DESC LIMIT 1
            )
        ''').fetchall()
        conn.close()
        return problem_facilities

class AlertsDB:
    """Database operations for alerts"""
    
    @staticmethod
    def get_active_alerts(limit: int = 10):
        """Get active alerts"""
        conn = get_db_connection()
        alerts = conn.execute('''
            SELECT a.*, f.name as facility_name
            FROM alerts a
            JOIN facilities f ON a.facility_id = f.id
            WHERE a.resolved = FALSE
            ORDER BY 
                CASE a.severity 
                    WHEN 'critical' THEN 1 
                    WHEN 'warning' THEN 2 
                    ELSE 3 
                END,
                a.created_at DESC
            LIMIT ?
        ''', (limit,)).fetchall()
        conn.close()
        return alerts
    
    @staticmethod
    def get_facility_alerts(facility_id: int, limit: int = 10):
        """Get alerts for a specific facility"""
        conn = get_db_connection()
        alerts = conn.execute('''
            SELECT * FROM alerts 
            WHERE facility_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (facility_id, limit)).fetchall()
        conn.close()
        return alerts
    
    @staticmethod
    def insert_alert(facility_id: int, alert_type: str, message: str, severity: str = 'info'):
        """Insert new alert"""
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO alerts (facility_id, alert_type, message, severity)
            VALUES (?, ?, ?, ?)
        ''', (facility_id, alert_type, message, severity))
        conn.commit()
        conn.close()
    
    @staticmethod
    def resolve_alert(alert_id: int):
        """Mark alert as resolved"""
        conn = get_db_connection()
        conn.execute('UPDATE alerts SET resolved = TRUE WHERE id = ?', (alert_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def check_existing_alert(facility_id: int, alert_type: str, hours: int = 1):
        """Check if similar alert already exists"""
        conn = get_db_connection()
        existing = conn.execute('''
            SELECT id FROM alerts 
            WHERE facility_id = ? AND alert_type = ? 
            AND resolved = FALSE AND created_at > datetime('now', '-{} hour')
        '''.format(hours), (facility_id, alert_type)).fetchone()
        conn.close()
        return existing is not None

class MessagesDB:
    """Database operations for messages"""
    
    @staticmethod
    def get_recent_messages(limit: int = 20):
        """Get recent messages"""
        conn = get_db_connection()
        messages = conn.execute('''
            SELECT m.*, 
                   f1.name as from_facility,
                   f2.name as to_facility
            FROM messages m
            JOIN facilities f1 ON m.from_facility_id = f1.id
            JOIN facilities f2 ON m.to_facility_id = f2.id
            ORDER BY m.created_at DESC
            LIMIT ?
        ''', (limit,)).fetchall()
        conn.close()
        return messages
    
    @staticmethod
    def insert_message(from_facility_id: int, to_facility_id: int, message: str, priority: str = 'normal'):
        """Insert new message"""
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO messages (from_facility_id, to_facility_id, message, priority)
            VALUES (?, ?, ?, ?)
        ''', (from_facility_id, to_facility_id, message, priority))
        conn.commit()
        conn.close()

def seed_sample_data():
    """Seed the database with sample facilities and initial data"""
    conn = get_db_connection()
    
    # Check if data already exists
    existing = conn.execute('SELECT COUNT(*) as count FROM facilities').fetchone()
    if existing['count'] > 0:
        conn.close()
        return
    
    # Sample facilities
    facilities = [
        ("Chicago Hub", "Chicago, IL", "hub", "active", 2000, 1200),
        ("Denver Station", "Denver, CO", "station", "active", 1000, 650),
        ("Atlanta Hub", "Atlanta, GA", "hub", "active", 2500, 1800),
        ("Phoenix Station", "Phoenix, AZ", "station", "active", 800, 400),
        ("Seattle Station", "Seattle, WA", "station", "active", 1200, 900),
        ("Miami Receiving", "Miami, FL", "receiving_point", "active", 500, 200)
    ]
    
    for facility in facilities:
        conn.execute('''
            INSERT INTO facilities (name, location, facility_type, status, max_capacity, current_load)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', facility)
    
    # Sample routes
    routes = [
        (1, 2, 920, 14.5),  # Chicago to Denver
        (1, 3, 720, 11.2),  # Chicago to Atlanta
        (2, 4, 430, 6.8),   # Denver to Phoenix
        (3, 6, 650, 10.1),  # Atlanta to Miami
        (2, 5, 870, 13.6)   # Denver to Seattle
    ]
    
    for route in routes:
        conn.execute('''
            INSERT INTO routes (from_facility_id, to_facility_id, distance_miles, estimated_time_hours)
            VALUES (?, ?, ?, ?)
        ''', route)
    
    conn.commit()
    conn.close()
