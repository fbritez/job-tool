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
