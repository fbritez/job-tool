from fastapi import APIRouter

from src.routers import jobs_router, search_router


def get_api():
    api_router = APIRouter()
    api_router.include_router(jobs_router.router, prefix='/jobs')
    api_router.include_router(search_router.router, prefix='/search')
    return api_router
