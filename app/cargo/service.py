from sqlalchemy import (
    delete,
    insert,
    select,
    update
)
from sqlalchemy.orm import aliased

from app.car.models import Car
from app.cargo.models import Cargo
from app.cargo.shemas import SCargo
from app.database import async_session_maker
from app.exceptions import (
    IncorrectDeliveryCodeException,
    IncorrectIDException,
    IncorrectPickupCodeException
)
from app.location.models import Location
from app.location.service import LocationService


class CargoService:

    @classmethod
    async def add(
            cls,
            zip_pickup: str,
            zip_delivery: str,
            weight: int,
            description: str
    ) -> SCargo:
        async with async_session_maker() as session:
            pickup_query = (
                select(Location.id)
                .where(Location.zip_code == zip_pickup)
            )

            delivery_query = (
                select(Location.id)
                .where(Location.zip_code == zip_delivery)
            )

            pickup_id = await session.execute(pickup_query)
            pickup_id = pickup_id.scalar_one_or_none()
            if not pickup_id:
                raise IncorrectPickupCodeException

            delivery_id = await session.execute(delivery_query)
            delivery_id = delivery_id.scalar_one_or_none()
            if not delivery_id:
                raise IncorrectDeliveryCodeException

            add_cargo = (
                insert(Cargo)
                .values(
                    pickup_id=pickup_id,
                    delivery_id=delivery_id,
                    weight=weight,
                    description=description
                )
                .returning(
                    Cargo.id,
                    Cargo.pickup_id,
                    Cargo.delivery_id,
                    Cargo.weight,
                    Cargo.description
                )
            )

            new_cargo = await session.execute(add_cargo)
            await session.commit()
            return new_cargo.mappings().one()

    @classmethod
    async def all(cls, max_weight=None, max_distance=None):
        async with async_session_maker() as session:
            pickup_location = aliased(Location)
            delivery_location = aliased(Location)

            cargo_query = (
                select(
                    Cargo.id,
                    Cargo.pickup_id,
                    Cargo.delivery_id,
                    Cargo.weight,
                    pickup_location.city.label("pickup_city"),
                    pickup_location.state.label("pickup_state"),
                    pickup_location.zip_code.label("pickup_zip_code"),
                    pickup_location.latitude.label("pickup_latitude"),
                    pickup_location.longitude.label("pickup_longitude"),
                    delivery_location.city.label("delivery_city"),
                    delivery_location.state.label("delivery_state"),
                    delivery_location.zip_code.label("delivery_zip_code"),
                    delivery_location.latitude.label("delivery_latitude"),
                    delivery_location.longitude.label("delivery_longitude")
                )
                .join(pickup_location, Cargo.pickup_id == pickup_location.id)
                .join(delivery_location, Cargo.delivery_id == delivery_location.id)
            )

            if max_weight is not None:
                cargo_query = cargo_query.where(Cargo.weight <= max_weight)
            if max_distance is None:
                max_distance = 450

            car_query = (
                select(
                    Car.load_capacity,
                    Location.longitude,
                    Location.latitude
                )
                .join(Location, Car.location_id == Location.id)
            )

            cargos = await session.execute(cargo_query)
            cargos = cargos.mappings().all()

            cars = await session.execute(car_query)
            cars = cars.mappings().all()

            cargo_info = []

            for cargo in cargos:
                cargo_location = (cargo.pickup_latitude, cargo.pickup_longitude)
                available_cars = 0

                for car in cars:
                    car_location = (car.latitude, car.longitude)
                    distance = await LocationService.get_distance(car_location, cargo_location)
                    if distance <= max_distance and car.load_capacity >= cargo.weight:
                        available_cars += 1

                cargo_info.append(
                    {
                        "id": cargo.id,
                        "pickup": {
                            "id": cargo.pickup_id,
                            "city": cargo.pickup_city,
                            "state": cargo.pickup_state,
                            "zip_code": cargo.pickup_zip_code,
                            "latitude": cargo.pickup_latitude,
                            "longitude": cargo.pickup_longitude
                        },
                        "delivery": {
                            "id": cargo.delivery_id,
                            "city": cargo.delivery_city,
                            "state": cargo.delivery_state,
                            "zip_code": cargo.delivery_zip_code,
                            "latitude": cargo.delivery_latitude,
                            "longitude": cargo.delivery_longitude
                        },
                        "available_cars": available_cars
                    }
                )

        return cargo_info

    @classmethod
    async def find_by_id(cls, cargo_id: int):
        async with async_session_maker() as session:
            pickup_location = aliased(Location)
            delivery_location = aliased(Location)

            cargo_query = (
                select(
                    Cargo.id,
                    Cargo.pickup_id,
                    Cargo.delivery_id,
                    Cargo.weight,
                    Cargo.description,
                    pickup_location.city.label("pickup_city"),
                    pickup_location.state.label("pickup_state"),
                    pickup_location.zip_code.label("pickup_zip_code"),
                    pickup_location.latitude.label("pickup_latitude"),
                    pickup_location.longitude.label("pickup_longitude"),
                    delivery_location.city.label("delivery_city"),
                    delivery_location.state.label("delivery_state"),
                    delivery_location.zip_code.label("delivery_zip_code"),
                    delivery_location.latitude.label("delivery_latitude"),
                    delivery_location.longitude.label("delivery_longitude")
                )
                .where(Cargo.id == cargo_id)
                .join(pickup_location, Cargo.pickup_id == pickup_location.id)
                .join(delivery_location, Cargo.delivery_id == delivery_location.id)
            )

            cargo = await session.execute(cargo_query)
            cargo = cargo.one_or_none()
            if not cargo:
                raise IncorrectIDException

            car_query = (
                select(
                    Car.number,
                    Location.latitude,
                    Location.longitude
                )
                .join(Location, Location.id == Car.location_id)
            )

            cars = await session.execute(car_query)
            cars = cars.mappings().all()

            cars_info = []
            cargo_location = (cargo.pickup_latitude, cargo.pickup_longitude)

            for car in cars:
                car_location = (car.latitude, car.longitude)
                distance = await LocationService.get_distance(car_location, cargo_location)
                info = {
                    "number": car.number,
                    "distance": round(distance, 1)
                }
                cars_info.append(info)

            cargo_info = {
                "pickup": {
                    "id": cargo.pickup_id,
                    "city": cargo.pickup_city,
                    "state": cargo.pickup_state,
                    "zip_code": cargo.pickup_zip_code,
                    "latitude": cargo.pickup_latitude,
                    "longitude": cargo.pickup_longitude
                },
                "delivery": {
                    "id": cargo.delivery_id,
                    "city": cargo.delivery_city,
                    "state": cargo.delivery_state,
                    "zip_code": cargo.delivery_zip_code,
                    "latitude": cargo.delivery_latitude,
                    "longitude": cargo.delivery_longitude
                },
                "weight": cargo.weight,
                "description": cargo.description,
                "cars": cars_info
            }
            return cargo_info

    @classmethod
    async def update(
            cls,
            cargo_id: int,
            weight: int,
            description: str
    ) -> SCargo:
        async with async_session_maker() as session:
            update_query = (
                update(Cargo)
                .where(Cargo.id == cargo_id)
                .values(weight=weight, description=description)
                .returning(
                    Cargo.id,
                    Cargo.pickup_id,
                    Cargo.delivery_id,
                    Cargo.weight,
                    Cargo.description
                )
            )
            updated_cargo = await session.execute(update_query)
            updated_cargo = updated_cargo.mappings().one_or_none()

            if not updated_cargo:
                raise IncorrectIDException

            await session.commit()
            return updated_cargo

    @classmethod
    async def delete(cls, cargo_id: int) -> None:
        async with async_session_maker() as session:
            delete_query = (
                delete(Cargo)
                .where(Cargo.id == cargo_id)
                .returning(Cargo.id)
            )
            is_deleted = await session.execute(delete_query)

            if not is_deleted.scalar_one_or_none():
                raise IncorrectIDException

            await session.commit()
