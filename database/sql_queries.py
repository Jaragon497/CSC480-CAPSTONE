# sql_queries.py - SQL Query Constants

# Table Creation Queries
CREATE_FACILITIES_TABLE = '''
    CREATE TABLE IF NOT EXISTS facilities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        facility_type TEXT NOT NULL,
        status TEXT DEFAULT 'active',
        max_capacity INTEGER DEFAULT 1000,
        current_load INTEGER DEFAULT 0,
        staff_count INTEGER DEFAULT 50,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
'''

CREATE_FACILITY_METRICS_TABLE = '''
    CREATE TABLE IF NOT EXISTS facility_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        facility_id INTEGER,
        staffing_level INTEGER,
        productivity_rate REAL,
        equipment_status TEXT,
        downtime_minutes INTEGER DEFAULT 0,
        delivery_timeliness REAL DEFAULT 95.0,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (facility_id) REFERENCES facilities (id)
    )
'''

CREATE_MESSAGES_TABLE = '''
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
'''

CREATE_ROUTES_TABLE = '''
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
'''

CREATE_ALERTS_TABLE = '''
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
'''

# Facility Queries
GET_ALL_ACTIVE_FACILITIES_WITH_METRICS = '''
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
'''

GET_FACILITY_BY_ID = 'SELECT * FROM facilities WHERE id = ?'

GET_ALL_ACTIVE_FACILITIES = 'SELECT * FROM facilities WHERE status = "active" ORDER BY name'

# Metrics Queries
INSERT_FACILITY_METRICS = '''
    INSERT INTO facility_metrics 
    (facility_id, staffing_level, productivity_rate, equipment_status, downtime_minutes, delivery_timeliness)
    VALUES (?, ?, ?, ?, ?, ?)
'''

GET_FACILITY_METRICS = '''
    SELECT * FROM facility_metrics 
    WHERE facility_id = ? 
    ORDER BY timestamp DESC 
    LIMIT ?
'''

GET_RECENT_PROBLEM_FACILITIES = '''
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
'''

# Alert Queries
GET_ACTIVE_ALERTS = '''
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
'''

GET_FACILITY_ALERTS = '''
    SELECT * FROM alerts 
    WHERE facility_id = ? 
    ORDER BY created_at DESC 
    LIMIT ?
'''

INSERT_ALERT = '''
    INSERT INTO alerts (facility_id, alert_type, message, severity)
    VALUES (?, ?, ?, ?)
'''

RESOLVE_ALERT = 'UPDATE alerts SET resolved = TRUE WHERE id = ?'

CHECK_EXISTING_ALERT = '''
    SELECT id FROM alerts 
    WHERE facility_id = ? AND alert_type = ? 
    AND resolved = FALSE AND created_at > datetime('now', '-{} hour')
'''

# Message Queries
GET_RECENT_MESSAGES = '''
    SELECT m.*, 
           f1.name as from_facility,
           f2.name as to_facility
    FROM messages m
    JOIN facilities f1 ON m.from_facility_id = f1.id
    JOIN facilities f2 ON m.to_facility_id = f2.id
    ORDER BY m.created_at DESC
    LIMIT ?
'''

INSERT_MESSAGE = '''
    INSERT INTO messages (from_facility_id, to_facility_id, message, priority)
    VALUES (?, ?, ?, ?)
'''

# Sample Data Insertion Queries
INSERT_FACILITY = '''
    INSERT INTO facilities (name, location, facility_type, status, max_capacity, current_load, staff_count)
    VALUES (?, ?, ?, ?, ?, ?, ?)
'''

INSERT_ROUTE = '''
    INSERT INTO routes (from_facility_id, to_facility_id, distance_miles, estimated_time_hours)
    VALUES (?, ?, ?, ?)
'''

COUNT_FACILITIES = 'SELECT COUNT(*) as count FROM facilities'