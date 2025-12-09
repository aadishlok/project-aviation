from fastapi import Request
from fastapi.responses import JSONResponse
from .errors import AppException


async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.code,
            "message": exc.message
        }
    )
