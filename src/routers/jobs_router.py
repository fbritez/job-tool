from typing import List, Union
import logging
from fastapi import APIRouter
from starlette.responses import JSONResponse
import starlette.status as status

from src.filter.filters import generate_filter
from src.model import JobPosition
from src.services.job_service import JobPositionService

router = APIRouter()

service = JobPositionService()


@router.post("")
def create_job(job_position: JobPosition):
    service.store(job_position)
    code = job_position.get_id()
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"message": f"Job code: {code} was created successfully"})


@router.get("", responses={status.HTTP_200_OK: {"jobs": List[JobPosition]}})
def all_jobs():
    jobs = service.get_all()
    return jobs


@router.get("/", responses={status.HTTP_200_OK: {"jobs": List[JobPosition]}})
def filter_jobs(title: Union[str, None] = '',
                description: Union[str, None] = '',
                salary_min: Union[int, None] = 0,
                salary_max: Union[int, None] = 0,
                country: Union[str, None] = '',
                tags: Union[List, None] = None):

    filters = generate_filter(title, description, salary_min, salary_max, country, tags)
    logging.info('Preparing filter for: %s', filters)
    jobs = service.filter_jobs(filters)

    return jobs


@router.get("/{job_id}", responses={status.HTTP_200_OK: {"job": JobPosition}})
def get_job(job_id: str):
    jobs = service.get_jobs_by_id(job_id)

    if not jobs:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"message": f"Job not found. Job Id: {job_id}"})

    return jobs[0]
