from fastapi import APIRouter

user_projects_router = APIRouter(
    prefix="/projects",
    tags=["teacher", "overseer", "projects"],
)

stats_projects_router = APIRouter(
    prefix="/stats",
    tags=["stats"],
)
