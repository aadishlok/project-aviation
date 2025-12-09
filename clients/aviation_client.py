from ..config import settings
import requests

ROUTES = {
    "GET_FLIGHT_STATUS": "/events"
}


class AviationClass:

    
    def __init__(self):
        self.API_URL = settings.AVIATION_DATA_API_URL
        self.API_TOKEN = settings.AVAIATION_DATA_API_TOKEN

    
    async def get_flight_status(self, flight_id: str):
        if not flight_id:
            raise ValueError("Flight id is required")
        
        url = self.API_URL + ROUTES["GET_FLIGHT_STATUS"]
        headers = {
            "authorization": "Bearer " + self.API_TOKEN
        }
        params = {
            "flightId": flight_id
        }

        print(f"Properties: {url} \n {headers} \n {params}")

        flight_response = requests.get(url=url, params=params, headers=headers)
        flight_response.raise_for_status()
        response = flight_response.json()
        print(f"\n\n FR: {response} \n\n")

        return response

