from typing import List, Union
from fastapi import APIRouter
import starlette.status as status
import logging
from src.model import JobPosition
from src.services.search_service import SearchService, ExternalSource

router = APIRouter()

service = SearchService([ExternalSource(source_url='http://127.0.0.1:8000/jobs/',
                                        search_field_mapping={'title': 'title',
                                                              'description': 'description',
                                                              'salary_min': 'salary_min',
                                                              'salary_max': 'salary_max',
                                                              'country': 'country',
                                                              'tags': 'tags'
                                                              },
                                        field_to_object_function=lambda job: JobPosition(id=job['id'],
                                                                                         title=job['title'],
                                                                                         description=job['description'],
                                                                                         salary=job['salary'],
                                                                                         country=job['country'],
                                                                                         tags=job['tags'])),
                         ExternalSource(source_url='http://localhost:8080/jobs',
                                        search_field_mapping={'title': 'name',
                                                              'salary_min': 'salary_min',
                                                              'salary_max': 'salary_max',
                                                              'country': 'country'
                                                              },
                                        field_to_object_function=lambda job: JobPosition(id='External Source',
                                                                                         title=job[0],
                                                                                         salary=job[1],
                                                                                         country=job[2],
                                                                                         tags=job[3]))])


def log_parameters(title, description, salary_min, salary_max, country, tags):
    values = ''
    if title:
        values = values + ' - title: ' + title
    if description:
        values = values + ' - description: ' + description
    if salary_min:
        values = values + ' - salary_min: ' + str(salary_min)
    if salary_max:
        values = values + ' - salary_max: ' + str(salary_max)
    if country:
        values = values + ' - country: ' + country
    if tags:
        values = values + ' - tags: ' + str(tags)

    logging.info('Seargh paramters: %s', values)


@router.get("/", responses={status.HTTP_200_OK: {"jobs": List[JobPosition]}})
def search_jobs(title: Union[str, None] = None,
                description: Union[str, None] = None,
                salary_min: Union[int, None] = None,
                salary_max: Union[int, None] = None,
                country: Union[str, None] = None,
                tags: Union[List, None] = None):
    log_parameters(title, description, salary_min, salary_max, country, tags)

    jobs = service.search_jobs(title, description, salary_min, salary_max, country, tags)

    logging.info('Found Jobs: %s', jobs)

    return jobs
