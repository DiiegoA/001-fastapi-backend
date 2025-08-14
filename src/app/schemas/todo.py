from pydantic import BaseModel
from typing import Optional

class TodoBase(BaseModel):
    name: Optional[str] = None
    completed: Optional[bool] = None

class TodoCreate(TodoBase):
    name: str
    completed: bool = False

class TodoUpdate(TodoBase):
    pass

class TodoRead(TodoBase):
    id: int

    class Config:
        from_attributes = True
