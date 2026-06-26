from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base
from app.enums import ChoreFieldType


class Chore(Base):
    __tablename__ = "chores"

    chore_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    
    # Stores a iCal RFC 5545 RRULE string or:
    # null = disabled, "auto" = automatic
    manual_cadence = Column(String(256), nullable=True) 
                            
    fields = relationship("ChoreField", cascade="all, delete-orphan", back_populates="chore")
    events = relationship("ChoreEvent", cascade="all, delete-orphan", back_populates="chore")

class ChoreField(Base):
    __tablename__ = "chore_fields"

    field_id = Column(Integer, primary_key=True, index=True) 
    chore_id = Column(Integer, ForeignKey("chores.chore_id", ondelete="CASCADE"), nullable=False)
    name = Column(String(128), nullable=False)
    value_type = Column(Enum(ChoreFieldType), nullable=False)

    chore = relationship("Chore", back_populates="fields")
    values = relationship("ChoreEventFieldValue", cascade="all, delete-orphan", back_populates="field")

class ChoreEvent(Base):
    __tablename__ = "chore_events"

    event_id = Column(Integer, primary_key=True, index=True) 
    chore_id = Column(Integer, ForeignKey("chores.chore_id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    notes = Column(Text, nullable=True)

    chore = relationship("Chore", back_populates="events")
    field_values = relationship("ChoreEventFieldValue", cascade="all, delete-orphan", back_populates="event")

class ChoreEventFieldValue(Base):
    __tablename__ = "chore_event_field_values"

    value_id = Column(Integer, primary_key=True, index=True) 
    event_id = Column(Integer, ForeignKey("chore_events.event_id", ondelete="CASCADE"), nullable=False)
    field_id = Column(Integer, ForeignKey("chore_fields.field_id", ondelete="CASCADE"), nullable=False)
    
    value = Column(Text, nullable=False)    # Stored as string, converted on the fly

    event = relationship("ChoreEvent", back_populates="field_values")
    field = relationship("ChoreField", back_populates="values")
