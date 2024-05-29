from fastapi import (
    APIRouter,
    status
)

from app.car.service import CarService
from app.car.shemas import (
    SCar,
    SCarUpdate
)

router = APIRouter(
    prefix="/car",
    tags=["Car"]
)


@router.patch(
    "/update/{car_id}",
    status_code=status.HTTP_200_OK
)
async def update_car(info: SCarUpdate) -> SCar:
    return await CarService.update(
        car_id=info.car_id,
        zip_code=info.zip_code
    )
