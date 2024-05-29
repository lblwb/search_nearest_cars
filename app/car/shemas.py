from pydantic import (
    BaseModel,
    Field
)


class SCar(BaseModel):
    id: int
    load_capacity: int = Field(ge=1, le=1000)
    location_id: int
    number: str


class SCarUpdate(BaseModel):
    car_id: int
    zip_code: str


class SCarInfo(BaseModel):
    number: str
    distance: float
