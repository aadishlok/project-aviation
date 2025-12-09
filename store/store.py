class FlightStateStore:

    def __init__(self):
        self.state = {}

    def get_state(self, flight_id: str):
        return self.state.get(flight_id)

    def update_state(self, flight_id: str, delay: int, event: dict):
        previous = self.state.get(flight_id)

        if previous:
            history = previous["history"] + [delay]
        else:
            history = [delay]

        self.state[flight_id] = {
            "last_delay": delay,
            "history": history,
            "last_event": event
        }

        return previous