from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String
)

from app.database import Base


class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True)
    load_capacity = Column(Integer, nullable=False)
    location_id = Column(ForeignKey("location.id"), nullable=False)
    number = Column(String, nullable=False, unique=True)
