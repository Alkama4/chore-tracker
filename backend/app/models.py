from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class LogGroup(Base):
    __tablename__ = "log_groups"

    group_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)

    items = relationship("LogItem", cascade="all, delete-orphan", back_populates="group")


class LogItem(Base):
    __tablename__ = "log_items"

    item_id = Column(Integer, primary_key=True, index=True)
    group_id = Column(
        Integer,
        ForeignKey("log_groups.group_id",
        ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name = Column(String(128), nullable=False)

    # iCal RFC 5545 RRULE string.
    # NULL means that no manual schedule is configured.
    schedule_rrule = Column(String(256), nullable=True)

    group = relationship("LogGroup", back_populates="items")
    fields = relationship("LogField", cascade="all, delete-orphan",back_populates="item")
    entries = relationship("LogEntry", cascade="all, delete-orphan",back_populates="item")


class LogField(Base):
    __tablename__ = "log_fields"

    field_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(
        Integer,
        ForeignKey("log_items.item_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name = Column(String(128), nullable=False)
    value_type = Column(String(32), nullable=False)

    item = relationship("LogItem", back_populates="fields")
    values = relationship("LogEntryValue", cascade="all, delete-orphan", back_populates="field")


class LogEntry(Base):
    __tablename__ = "log_entries"

    entry_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(
        Integer,
        ForeignKey("log_items.item_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    logged_at = Column(DateTime(timezone=True), nullable=False, index=True)
    notes = Column(Text, nullable=True)

    item = relationship("LogItem", back_populates="entries")
    field_values = relationship("LogEntryValue", cascade="all, delete-orphan", back_populates="entry")


class LogEntryValue(Base):
    __tablename__ = "log_entry_values"

    value_id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(
        Integer,
        ForeignKey("log_entries.entry_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    field_id = Column(
        Integer,
        ForeignKey("log_fields.field_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Only one of these should contain the actual value.
    value_text = Column(Text, nullable=True)
    value_int = Column(Integer, nullable=True)
    value_float = Column(Float, nullable=True)
    value_bool = Column(Boolean, nullable=True)

    entry = relationship("LogEntry", back_populates="field_values")
    field = relationship("LogField", back_populates="values")

    __table_args__ = (
        UniqueConstraint(
            "entry_id",
            "field_id",
            name="uq_log_entry_field",
        ),
    )
