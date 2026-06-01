import os
import sys
import subprocess

if __name__ == "__main__":
    # Get absolute path to applications/frontend/main.py
    frontend_main = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'applications', 'frontend', 'main.py'
    ))
    
    # Run using the current python executable
    print(f"Launching Designer Tool Frontend Server from root...")
    try:
        subprocess.run([sys.executable, frontend_main], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Failed to start server: {e}")
