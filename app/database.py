import sqlite3
from datetime import datetime
import os

# We point the database to the 'data' folder we created earlier
DB_PATH = os.path.join("data", "sentinel_vault.db")

def init_db():
    """Initializes the SQLite database and creates the security_logs table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # We use a structured SQL table to track every intrusion
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS security_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"🗄️ Database initialized at: {DB_PATH}")

def log_security_event(device_id, event_type, severity, description):
    """Inserts a detected security threat into the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO security_logs (device_id, event_type, severity, description, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (device_id, event_type, severity, description, datetime.now()))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database Error: {e}")
        return False

def get_all_alerts():
    """Helper function to fetch all logged threats (useful for your portfolio)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM security_logs ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows