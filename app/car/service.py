import random
from string import (
    ascii_uppercase,
    digits
)

from sqlalchemy import (
    select,
    update
)

from app.car.models import Car
from app.car.shemas import SCar
from app.database import async_session_maker
from app.exceptions import (
    IncorrectCodeException,
    IncorrectIDException
)
from app.location.models import Location


class CarService:

    @classmethod
    async def update(cls, car_id: int, zip_code: str) -> SCar:
        async with async_session_maker() as session:
            car_query = (
                select(Car.id)
                .where(Car.id == car_id)
            )
            car = await session.execute(car_query)
            car = car.scalar_one_or_none()
            if not car:
                raise IncorrectIDException

            location_query = (
                select(Location.id)
                .where(Location.zip_code == zip_code)
            )
            location_id = await session.execute(location_query)
            location_id = location_id.scalar_one_or_none()
            if not location_id:
                raise IncorrectCodeException

            update_query = (
                update(Car)
                .where(Car.id == car_id)
                .values(location_id=location_id)
                .returning(
                    Car.id,
                    Car.load_capacity,
                    Car.location_id,
                    Car.number
                )
            )
            updated_car = await session.execute(update_query)
            await session.commit()

            return updated_car.mappings().one()

    @classmethod
    async def get_unique_number(cls) -> str:
        number = cls._generate_car_number()
        existing_numbers = await cls._get_all_numbers()
        while number in existing_numbers:
            number = cls._generate_car_number()
        return number

    @staticmethod
    def _generate_car_number() -> str:
        random_numbers = "".join(random.choices(digits, k=4))
        random_letter = random.choice(ascii_uppercase)
        return random_numbers + random_letter

    @staticmethod
    async def _get_all_numbers() -> set:
        async with async_session_maker() as session:
            query = select(Car.number)
            instances = await session.execute(query)
            numbers = {num[0] for num in instances.fetchall()}

        return numbers
