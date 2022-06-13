from typing import List, Union

from fastapi import APIRouter
from starlette.responses import JSONResponse
import starlette.status as status

from src.model import JobPosition
from src.services.search_service import SearchService

router = APIRouter()

service = SearchService([])

@router.get("/jobs/", responses={status.HTTP_200_OK: {"jobs": List[JobPosition]}})
def search_jobs(title: Union[str, None] = None, description: Union[str, None] = None):
    pass