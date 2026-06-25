from sqlalchemy import Column, Integer
from app.database import Base


class Chore(Base):
    __tablename__ = "chores"

    chore_id = Column(Integer, primary_key=True, index=True)
