from fastapi import FastAPI

from app.car.routers import router as car_router
from app.cargo.routers import router as cargo_router
from app.service import FillDb

app = FastAPI(
    title="Search nearest vehicles",
    root_path="/api"
)


@app.on_event("startup")
async def startup() -> None:
    await FillDb.locations()
    await FillDb.cars()


app.include_router(car_router)
app.include_router(cargo_router)
