from fastapi import APIRouter
from starlette.responses import JSONResponse
import json
import starlette.status as status

from src.model import JobPosition
from src.job_service import JobPositionService

router = APIRouter()

service = JobPositionService()


@router.post("")
def create_job(job_position: JobPosition):
    service.store(job_position)
    code = job_position.get_id()
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"message": f"Job code:{code} was created successfully"})


@router.get("")
def all_jobs():
    jobs = service.get_all()
    '''return JSONResponse(status_code=status.HTTP_200_OK,
                        content=json.dumps(jobs))
    '''
    return jobs


@router.get("/{job_id}", responses={status.HTTP_200_OK: {"job": JobPosition}})
def get_job(job_id: str):
    job = service.get_job_by_id(job_id)

    if not job:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=f"message: Job not found. Job Id: {job_id}")

    return job
