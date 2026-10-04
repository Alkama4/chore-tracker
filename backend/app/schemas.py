from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.enums import LogFieldType


# -------------------------
# Log Group
# -------------------------

class LogGroupBase(BaseModel):
    name: str


class LogGroupCreate(LogGroupBase):
    pass


class LogGroupReplace(LogGroupBase):
    pass


class LogGroupRead(LogGroupBase):
    group_id: int

    model_config = ConfigDict(from_attributes=True)


class LogGroupReadList(BaseModel):
    groups: List[LogGroupRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Log Field
# -------------------------

class LogFieldBase(BaseModel):
    name: str
    value_type: LogFieldType


class LogFieldCreate(LogFieldBase):
    pass


class LogFieldReplace(LogFieldBase):
    field_id: Optional[int] = None


class LogFieldRead(LogFieldBase):
    field_id: int

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Log Item
# -------------------------

class LogItemBase(BaseModel):
    group_id: int
    name: str
    schedule_rrule: Optional[str] = None


class LogItemCreate(LogItemBase):
    fields: List[LogFieldCreate] = Field(default_factory=list)


class LogItemReplace(LogItemBase):
    fields: List[LogFieldReplace] = Field(default_factory=list)


class LogItemRead(LogItemBase):
    item_id: int
    fields: List[LogFieldRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class LogItemReadList(BaseModel):
    items: List[LogItemRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Log Entry Value
# -------------------------

class LogEntryValueBase(BaseModel):
    field_id: int
    value: str  # Inputted as string, the application converts it according to LogFieldType.


class LogEntryValueCreate(LogEntryValueBase):
    pass


class LogEntryValueReplace(LogEntryValueBase):
    value_id: int


class LogEntryValueRead(BaseModel):
    value_id: int
    field_id: int
    field: LogFieldRead

    value: str

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Log Entry
# -------------------------

class LogEntryBase(BaseModel):
    item_id: int
    logged_at: datetime
    notes: Optional[str] = None


class LogEntryCreate(LogEntryBase):
    field_values: List[LogEntryValueCreate] = Field(default_factory=list)


class LogEntryReplace(LogEntryBase):
    entry_id: int
    field_values: List[LogEntryValueReplace] = Field(default_factory=list)


class LogEntryRead(LogEntryBase):
    entry_id: int
    field_values: List[LogEntryValueRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class LogEntryReadList(BaseModel):
    entries: List[LogEntryRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Generic
# -------------------------

class ConfirmationResponse(BaseModel):
    id: int
    success: bool
    msg: str
