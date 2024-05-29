from pydantic import (
    BaseModel,
    Field
)


class SLocation(BaseModel):
    id: int
    city: str
    state: str
    zip_code: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
