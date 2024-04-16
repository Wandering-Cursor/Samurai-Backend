from fastapi import APIRouter

communication_router = APIRouter(
    prefix="/communication",
    tags=[
        "student",
        "teacher",
        "communication",
    ],
)
