import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
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
            "db_host": "localhost",
            "db_port": 5432,
            "db_name": "designer_tool",
            "db_user": "postgres",
            "db_password": "password",
            "debug": True
        }

config = load_config()

def get_db_connection():
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host=config.get("db_host", "localhost"),
            port=config.get("db_port", 5432),
            database=config.get("db_name", "designer_tool"),
            user=config.get("db_user", "postgres"),
            password=config.get("db_password", "password")
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"[ERROR] Failed to connect to PostgreSQL: {e}")
        raise

def init_db():
    """Initialize PostgreSQL database and create tables if they don't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Create projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                tag TEXT DEFAULT 'Select',
                project_type TEXT NOT NULL,
                date_created TEXT NOT NULL,
                accuracy INTEGER DEFAULT 0,
                dataset_preview TEXT,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Check if table is empty, and seed it if it is
        cursor.execute("SELECT COUNT(*) FROM projects")
        if cursor.fetchone()[0] == 0:
            # Seed initial projects
            initial_projects = [
                ("crate_tracker_test", "Select", "Object Detection", "25 Apr 2024, 10:04 am", 77, "crate1,crate2,crate3", "active"),
                ("safety_helmet_classifier", "Urgent", "Classification", "12 May 2026, 02:30 pm", 92, "helmet1,helmet2", "active"),
                ("conveyor_anomaly_segmentation", "Review", "Segmentation", "28 May 2026, 11:15 am", 84, "conveyor1,conveyor2,conveyor3", "active"),
                ("old_leak_detector", "Select", "Object Detection", "10 Jan 2024, 09:00 am", 65, "leak1", "old"),
                ("corrupted_training_run", "Select", "Classification", "05 Feb 2026, 04:00 pm", 0, "", "trash")
            ]
            
            cursor.executemany('''
                INSERT INTO projects (name, tag, project_type, date_created, accuracy, dataset_preview, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', initial_projects)
        
        conn.commit()
        print("[INFO] Database initialized successfully.")
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to initialize database: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def get_all_projects(status='active'):
    """Get all projects with a specific status"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("SELECT * FROM projects WHERE status = %s ORDER BY id DESC", (status,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        cursor.close()
        conn.close()

def get_project_stats():
    """Get statistics for all project statuses"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        stats = {}
        for s in ['active', 'old', 'trash']:
            cursor.execute("SELECT COUNT(*) FROM projects WHERE status = %s", (s,))
            stats[s] = cursor.fetchone()[0]
        return stats
    finally:
        cursor.close()
        conn.close()

def add_project(name, project_type, tag='Select', accuracy=0, dataset_preview=''):
    """Add a new project to the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    date_str = datetime.now().strftime("%d %b %Y, %I:%M %p").lower()
    
    try:
        cursor.execute('''
            INSERT INTO projects (name, tag, project_type, date_created, accuracy, dataset_preview, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'active')
            RETURNING id
        ''', (name, tag, project_type, date_str, accuracy, dataset_preview))
        
        project_id = cursor.fetchone()[0]
        conn.commit()
        return {"success": True, "project_id": project_id}
    except psycopg2.IntegrityError as e:
        conn.rollback()
        return {"success": False, "error": f"Project named '{name}' already exists."}
    except Exception as e:
        conn.rollback()
        return {"success": False, "error": str(e)}
    finally:
        cursor.close()
        conn.close()

def update_project_tag(project_id, tag):
    """Update the tag of a project"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE projects SET tag = %s WHERE id = %s", (tag, project_id))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to update project tag: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def update_project_status(project_id, status):
    """Update the status of a project"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE projects SET status = %s WHERE id = %s", (status, project_id))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to update project status: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_project_permanently(project_id):
    """Permanently delete a project from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM projects WHERE id = %s", (project_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to delete project: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
