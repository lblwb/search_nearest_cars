from sqlalchemy import (
    select,
    update
)

from app.car.models import Car
from app.database import async_session_maker
from app.location.service import LocationService


async def refresh_car_location() -> None:
    async with async_session_maker() as session:
        car_query = select(Car.id, Car.location_id)
        cars = await session.execute(car_query)
        cars = cars.mappings().all()

        for car in cars:
            random_location = await LocationService.get_random_location()
            while random_location == car.location_id:
                random_location = await LocationService.get_random_location()

            update_query = (
                update(Car)
                .where(Car.id == car.id)
                .values(location_id=random_location)
            )
            await session.execute(update_query)
        await session.commit()
