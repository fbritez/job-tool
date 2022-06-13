from pydantic import BaseModel
from typing import Union, List


class JobPosition(BaseModel):
    id: Union[str, None] = ''
    title: str
    description: Union[str, None] = ''
    salary: Union[int, None] = 0
    country: Union[str, None] = ''
    tags: Union[List, None] = []

    def get_id(self):
        return self.id


class SubscriptionDTO(BaseModel):
    email: str
    title: str
    description: Union[str, None] = ''
    salary_min: Union[int, None] = None
    salary_max: Union[int, None] = None
    country: Union[str, None] = None
    tags: Union[List, None] = []


class Subscription:
    email: str
    filters: Union[List, None] = []

    def __init__(self, email, filters):
        self.email = email
        self.filters = filters

    def match_with(self, job_position):
        filtered_jobs = [job_position]
        for filter_object in self.filters:
            filtered_jobs = filter_object.filter(filtered_jobs)

        return bool(filtered_jobs)
