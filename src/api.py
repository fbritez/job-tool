from fastapi import APIRouter

from src.routers import jobs


def get_api():
    api_router = APIRouter()
    api_router.include_router(jobs.router, prefix='/jobs')

    return api_router
