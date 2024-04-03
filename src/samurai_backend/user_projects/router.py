from fastapi import APIRouter

user_projects_router = APIRouter(
    prefix="/projects",
    tags=["teacher", "overseer", "projects"],
)
