import os
import json
import sqlite3
from datetime import datetime

# Load configuration
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.json')

def load_config():
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except Exception:
        return {
            "app_name": "FirstStep.ai Designer",
            "host": "127.0.0.1",
            "port": 8080,
            "db_path": "applications/frontend/databases/projects.db",
            "debug": True
        }

config = load_config()
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '..', config.get("db_path", "applications/frontend/databases/projects.db")))

def get_db_connection():
    # Ensure directory exists
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            tag TEXT DEFAULT 'Select',
            project_type TEXT NOT NULL,
            date_created TEXT NOT NULL,
            accuracy INTEGER DEFAULT 0,
            dataset_preview TEXT,
            status TEXT DEFAULT 'active'
        )
    ''''')
    
    # Check if table is empty, and seed it if it is
    cursor.execute("SELECT COUNT(*) FROM projects")
    if cursor.fetchone()[0] == 0:
        # Seed initial project matching Image 2
        now_str = datetime.now().strftime("%d %b %Y, %I:%M %p") # e.g. "25 Apr 2024, 10:04 am"
        
        initial_projects = [
            ("crate_tracker_test", "Select", "Object Detection", "25 Apr 2024, 10:04 am", 77, "crate1,crate2,crate3", "active"),
            ("safety_helmet_classifier", "Urgent", "Classification", "12 May 2026, 02:30 pm", 92, "helmet1,helmet2", "active"),
            ("conveyor_anomaly_segmentation", "Review", "Segmentation", "28 May 2026, 11:15 am", 84, "conveyor1,conveyor2,conveyor3", "active"),
            ("old_leak_detector", "Select", "Object Detection", "10 Jan 2024, 09:00 am", 65, "leak1", "old"),
            ("corrupted_training_run", "Select", "Classification", "05 Feb 2026, 04:00 pm", 0, "", "trash")
        ]
        
        cursor.executemany('''
            INSERT INTO projects (name, tag, project_type, date_created, accuracy, dataset_preview, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', initial_projects)
        
    conn.commit()
    conn.close()

def get_all_projects(status='active'):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects WHERE status = ? ORDER BY id DESC", (status,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_project_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    stats = {}
    for s in ['active', 'old', 'trash']:
        cursor.execute("SELECT COUNT(*) FROM projects WHERE status = ?", (s,))
        stats[s] = cursor.fetchone()[0]
        
    conn.close()
    return stats

def add_project(name, project_type, tag='Select', accuracy=0, dataset_preview=''):
    conn = get_db_connection()
    cursor = conn.cursor()
    date_str = datetime.now().strftime("%d %b %Y, %I:%M %p").lower()
    
    try:
        cursor.execute('''
            INSERT INTO projects (name, tag, project_type, date_created, accuracy, dataset_preview, status)
            VALUES (?, ?, ?, ?, ?, ?, 'active')
        ''', (name, tag, project_type, date_str, accuracy, dataset_preview))
        conn.commit()
        project_id = cursor.lastrowid
        conn.close()
        return {"success": True, "project_id": project_id}
    except sqlite3.IntegrityError:
        conn.close()
        return {"success": False, "error": f"Project named '{name}' already exists."}
    except Exception as e:
        conn.close()
        return {"success": False, "error": str(e)}

def update_project_tag(project_id, tag):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE projects SET tag = ? WHERE id = ?", (tag, project_id))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False

def update_project_status(project_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE projects SET status = ? WHERE id = ?", (status, project_id))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False

def delete_project_permanently(project_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False
