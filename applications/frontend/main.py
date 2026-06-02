from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uvicorn
import os
import sys

# Ensure applications/frontend is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import utils, utils_routes

# Load config
config = utils.load_config()

app = FastAPI(
    title=config.get("app_name", "FirstStep.ai Designer"),
    description="A sleek and premium Designer Tool dashboard powered by FastAPI and Jinja2 templates.",
    version="1.0.0"
)

# Mount static folder
STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(os.path.join(STATIC_DIR, 'css'), exist_ok=True)
    os.makedirs(os.path.join(STATIC_DIR, 'js'), exist_ok=True)
    os.makedirs(os.path.join(STATIC_DIR, 'images'), exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Include routes
app.include_router(utils_routes.router)

@app.on_event("startup")
def startup_event():
    # Initialize the database
    try:
        utils.init_db()
        print("[SUCCESS] Database initialized successfully.")
    except Exception as e:
        print(f"[WARNING] Database connection failed: {e}")
        print("[INFO] Server starting anyway - please check your PostgreSQL connection.")

if __name__ == "__main__":
    host = config.get("host", "127.0.0.1")
    port = config.get("port", 8080)
    print(f"Starting server on http://{host}:{port}...")
    uvicorn.run("main:app", host=host, port=port, reload=True)
