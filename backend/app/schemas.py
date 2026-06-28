from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from app.enums import ChoreFieldType


# ---- Chore Field ----

class ChoreFieldBase(BaseModel):
    name: str
    value_type: ChoreFieldType

class ChoreFieldCreate(ChoreFieldBase):
    pass

class ChoreFieldReplace(ChoreFieldBase):
    field_id: int

class ChoreFieldRead(ChoreFieldBase):
    field_id: int
    
    model_config = ConfigDict(from_attributes=True)


# ---- Chore ----

class ChoreBase(BaseModel):
    name: str
    manual_cadence: Optional[str] = None

class ChoreCreate(ChoreBase):
    fields: Optional[List[ChoreFieldCreate]] = []

class ChoreReplace(ChoreBase):
    fields: Optional[List[ChoreFieldReplace]] = []

class ChoreRead(ChoreBase):
    chore_id: int
    fields: Optional[List[ChoreFieldRead]] = []
    
    model_config = ConfigDict(from_attributes=True)

class ChoreReadList(BaseModel):
    chores: Optional[List[ChoreRead]] = []

    model_config = ConfigDict(from_attributes=True)


# ---- Chore Event Field ----

class ChoreEventFieldBase(BaseModel):
    field_id: int
    value: str

class ChoreEventFieldCreate(ChoreEventFieldBase):
    pass

class ChoreEventFieldReplace(ChoreEventFieldBase):
    value_id: int

class ChoreEventFieldRead(ChoreEventFieldBase):
    field: ChoreFieldRead
    value_id: int
    
    model_config = ConfigDict(from_attributes=True)


# ---- Chore Event ----

class ChoreEventBase(BaseModel):
    chore_id: int
    date: date
    notes: Optional[str] = None

class ChoreEventCreate(ChoreEventBase):
    field_values: Optional[List[ChoreEventFieldCreate]] = []

class ChoreEventReplace(ChoreEventBase):
    event_id: int
    field_values: Optional[List[ChoreEventFieldReplace]] = []

class ChoreEventRead(ChoreEventBase):
    event_id: int
    field_values: Optional[List[ChoreEventFieldRead]] = []
    
    model_config = ConfigDict(from_attributes=True)


# ---- Generic ----

class ConfirmationResponse(BaseModel):
    id: int
    success: bool
    msg: str
