import random

from geopy.distance import distance
from sqlalchemy import select

from app.database import async_session_maker
from app.location.models import Location


class LocationService:

    @classmethod
    async def get_distance(
            cls,
            car_location: tuple[float, float],
            cargo_location: tuple[float, float],
    ) -> float:
        return distance(car_location, cargo_location).miles

    @classmethod
    async def get_random_location(cls) -> int:
        async with async_session_maker() as session:
            query = select(Location.id)
            instances = await session.execute(query)
            locations = instances.fetchall()

        return random.choice(locations)[0]
