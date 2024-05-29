from fastapi import (
    APIRouter,
    Depends,
    status
)

from app.cargo.service import CargoService
from app.cargo.shemas import (
    SCargo,
    SCargoAdd,
    SCargoAll,
    SCargoFilters,
    SCargoOne,
    SCargoUpdate
)
from app.exceptions import CargoCannotBeCreated

router = APIRouter(
    prefix="/cargo",
    tags=["Cargo"]
)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK
)
async def get_cargo_list(
        filters: SCargoFilters = Depends()
) -> list[SCargoAll]:
    return await CargoService.all(
        max_weight=filters.max_weight,
        max_distance=filters.max_distance
    )


@router.get(
    "/{cargo_id}",
    status_code=status.HTTP_200_OK
)
async def get_cargo_with_cars(cargo_id: int) -> SCargoOne:
    return await CargoService.find_by_id(cargo_id)


@router.post(
    "/add",
    status_code=status.HTTP_201_CREATED
)
async def add_cargo(cargo: SCargoAdd) -> SCargo:
    new_cargo = await CargoService.add(
        zip_pickup=cargo.zip_pickup,
        zip_delivery=cargo.zip_delivery,
        weight=cargo.weight,
        description=cargo.description
    )

    if not new_cargo:
        raise CargoCannotBeCreated

    return new_cargo


@router.patch(
    "/{cargo_id}",
    status_code=status.HTTP_200_OK
)
async def update_cargo(info: SCargoUpdate) -> SCargo:
    return await CargoService.update(
        cargo_id=info.cargo_id,
        weight=info.weight,
        description=info.description
    )


@router.delete(
    "/delete/{cargo_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_cargo(cargo_id: int) -> None:
    await CargoService.delete(cargo_id)
