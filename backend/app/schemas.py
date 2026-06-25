from typing import List, Optional
from pydantic import BaseModel


class ChoreOut(BaseModel):
    chore_id: int

    class Config:
        from_attributes = True
