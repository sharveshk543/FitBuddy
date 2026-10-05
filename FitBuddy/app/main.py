from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import create_tables
from app.services.gemini_generator import generate_workout_gemini
from app.services.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.services.updated_plan import update_workout_plan


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="FitBuddy",
    description="AI-powered personalized fitness assistant",
    version="1.0.0",
    lifespan=lifespan,
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)


# Jinja templates
templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )


@app.post("/generate", response_class=HTMLResponse)
async def generate_plan(
    request: Request,
    username: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    workout_plan = generate_workout_gemini(
        username=username,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity,
    )

    nutrition_tip = generate_nutrition_tip_with_flash(
        username=username,
        age=age,
        weight=weight,
        goal=goal,
    )

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "username": username,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip,
        },
    )


@app.post("/update-plan", response_class=HTMLResponse)
async def update_plan(
    request: Request,
    username: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    current_plan: str = Form(...),
):
    updated_plan = update_workout_plan(
        username=username,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity,
        current_plan=current_plan,
    )

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "username": username,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": updated_plan,
            "nutrition_tip": "",
        },
    )


@app.get("/users", response_class=HTMLResponse)
async def all_users(request: Request):
    """
    Display all saved users.
    """

    try:
        from app.database import get_all_users

        users = get_all_users()

    except Exception:
        users = []

    return templates.TemplateResponse(
        "all_users.html",
        {
            "request": request,
            "users": users,
        },
    )


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "application": "FitBuddy",
    }