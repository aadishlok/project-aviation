from .base_validator import BaseValidator
from ..errors.errors import ValidationException


class FlightValidator(BaseValidator):
    
    def validate(self, flight_id: str):
        if not flight_id:
            raise ValidationException("Flight ID is required")

        if not isinstance(flight_id, str):
            raise ValidationException("Flight ID must be a string")

        return True
