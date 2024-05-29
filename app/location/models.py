from sqlalchemy import (
    Column,
    Float,
    Integer,
    String
)

from app.database import Base


class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
