from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String
)

from app.database import Base


class Cargo(Base):
    __tablename__ = "cargo"

    id = Column(Integer, primary_key=True)
    pickup_id = Column(ForeignKey("location.id"), nullable=False)
    delivery_id = Column(ForeignKey("location.id"), nullable=False)
    weight = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
