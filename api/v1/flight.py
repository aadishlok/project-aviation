from fastapi import APIRouter, Query
from ...services.flight_status_service import FlightStatusService

router = APIRouter(prefix="/flight", tags=["Flight"])

service = FlightStatusService()

@router.get("/")
async def get_flight_status(flight_id: str = Query(None)):
    return await service.get_flight_status(flight_id)
