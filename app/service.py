import csv
import random

from sqlalchemy import insert

from app.car.models import Car
from app.car.service import CarService
from app.database import async_session_maker
from app.location.models import Location
from app.location.service import LocationService


class FillDb:
    CARS_QUANTITY = 20
    LOCATIONS_PATH = "app/data/uszips.csv"

    @classmethod
    async def locations(cls) -> None:
        with open(cls.LOCATIONS_PATH) as file:
            locations = csv.DictReader(file)

            async with async_session_maker() as session:
                for row in locations:
                    add_location = (
                        insert(Location)
                        .values(
                            city=row["city"],
                            state=row["state_name"],
                            zip_code=row["zip"],
                            latitude=float(row["lat"]),
                            longitude=float(row["lng"])
                        )
                    )
                    await session.execute(add_location)
                await session.commit()

    @classmethod
    async def cars(cls) -> None:
        async with async_session_maker() as session:
            for _ in range(cls.CARS_QUANTITY):
                load_capacity = random.randint(1, 1000)
                location_id = await LocationService.get_random_location()
                number = await CarService.get_unique_number()

                add_car = (
                    insert(Car)
                    .values(
                        load_capacity=load_capacity,
                        location_id=location_id,
                        number=number
                    )
                )
                await session.execute(add_car)
            await session.commit()
