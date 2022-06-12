from pydantic import BaseModel
from typing import Union


class JobPosition(BaseModel):
    id: Union[str, None] = None
    title: str
    description: Union[str, None] = None

    def get_id(self):
        return self.id
