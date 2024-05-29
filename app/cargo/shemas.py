from typing import Optional

from pydantic import (
    BaseModel,
    Field
)

from app.car.shemas import SCarInfo
from app.location.shemas import SLocation


class SCargo(BaseModel):
    id: int
    pickup_id: int
    delivery_id: int
    weight: int = Field(ge=1, le=1000)
    description: str = Field(min_length=5, max_length=255)


class SCargoFilters(BaseModel):
    max_weight: Optional[int] = Field(
        None,
        ge=1,
        le=1000,
        description="Filter by max weight"
    )
    max_distance: Optional[int] = Field(
        None,
        ge=1,
        description="Filter by max distance"
    )


class SCargoAdd(BaseModel):
    zip_pickup: str
    zip_delivery: str
    weight: int = Field(ge=1, le=1000)
    description: str = Field(min_length=5, max_length=255)


class SCargoOne(BaseModel):
    pickup: SLocation
    delivery: SLocation
    weight: int = Field(ge=1, le=1000)
    description: str = Field(min_length=5, max_length=255)
    cars: list[SCarInfo]


class SCargoUpdate(BaseModel):
    cargo_id: int
    weight: int = Field(ge=1, le=1000)
    description: str = Field(min_length=5, max_length=255)


class SCargoAll(BaseModel):
    id: int
    pickup: SLocation
    delivery: SLocation
    available_cars: int
