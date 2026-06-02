from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
import random
from . import utils

router = APIRouter()

# Set up templates path
TEMPLATES_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'))
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/", response_class=HTMLResponse)
async def view_dashboard(request: Request, status: str = "active"):
    # Ensure database is initialized
    utils.init_db()
    
    projects = utils.get_all_projects(status=status)
    stats = utils.get_project_stats()
    
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "projects": projects,
            "stats": stats,
            "current_status": status,
            "app_name": utils.config.get("app_name", "FirstStep.ai Designer")
        }
    )


@router.get("/projects/create", response_class=HTMLResponse)
async def create_project_page(request: Request):

    return RedirectResponse(url="/")

@router.post("/projects/create")
async def create_new_project(
    name: str = Form(...), 
    project_type: str = Form(...),
    tag: str = Form("Select")
):
    name = name.strip()
    if not name:
        return RedirectResponse(url="/?error=Name+cannot+be+empty", status_code=303)
        
    # Generate some mock dataset preview placeholders
    # In a real app we would upload files, here we mock it based on project type
    preview_images = "img1,img2,img3" if project_type == "Object Detection" else "img1,img2"
    
    # Generate random accuracy for visual flair
    import random
    accuracy = random.randint(65, 98) if "old" not in name.lower() else random.randint(40, 70)
    
    result = utils.add_project(name, project_type, tag, accuracy, preview_images)
    
    if result["success"]:
        return RedirectResponse(url="/", status_code=303)
    else:
        # Redirect with error
        from urllib.parse import quote
        return RedirectResponse(url=f"/?error={quote(result['error'])}", status_code=303)

@router.post("/api/projects/{project_id}/tag")
async def update_tag(project_id: int, data: dict):
    tag = data.get("tag", "Select")
    success = utils.update_project_tag(project_id, tag)
    if success:
        return {"success": True}
    raise HTTPException(status_code=400, detail="Failed to update tag")

@router.post("/projects/{project_id}/status")
async def change_project_status(project_id: int, status: str = Form(...)):
    if status not in ["active", "old", "trash"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    success = utils.update_project_status(project_id, status)
    if success:
        return RedirectResponse(url=f"/?status={status}", status_code=303)
    
    raise HTTPException(status_code=400, detail="Failed to update status")

@router.post("/projects/{project_id}/delete")
async def delete_project(project_id: int, current_status: str = Form("trash")):
    success = utils.delete_project_permanently(project_id)
    if success:
        return RedirectResponse(url=f"/?status={current_status}", status_code=303)
    raise HTTPException(status_code=400, detail="Failed to delete project")

@router.get("/projects/{project_id}", response_class=HTMLResponse)
async def view_project_dataset(request: Request, project_id: int):
    """View project dataset and workspace"""
    utils.init_db()
    
    # Get project details
    conn = utils.get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM projects WHERE id = %s", (project_id,))
        project_row = cursor.fetchone()
        if not project_row:
            raise HTTPException(status_code=404, detail="Project not found")
        project = dict(project_row) if hasattr(project_row, 'keys') else project_row
    finally:
        cursor.close()
        conn.close()
    
    # Generate mock dataset images
    dataset_images = []
    for i in range(1, 9):
        dataset_images.append({
            "id": i,
            "name": f"image_{i:04d}.jpg",
            "date_added": "25 Apr 2024, 10:08 am",
            "last_updated": "25 Apr 2024, 10:08 am",
            "annotated": random.choice([True, False]),
            "labels": "bottle, crate" if random.choice([True, False]) else ""
        })
    
    return templates.TemplateResponse(
        request=request,
        name="dataset.html",
        context={
            "project": project,
            "dataset_images": dataset_images,
            "app_name": utils.config.get("app_name", "FirstStep.ai Designer")
        }
    )
