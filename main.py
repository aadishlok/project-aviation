from fastapi import FastAPI
from .api.v1.flight import router as flight_router

app = FastAPI(title="Flight Status System")

app.include_router(flight_router)
