from datetime import datetime
from ..clients.aviation_client import AviationClass
from ..store.store import FlightStateStore
from ..validators.flight_validator import FlightValidator

store = FlightStateStore()

class FlightStatusService:

    def __init__(self):
        self.client = AviationClass()
        self.validator = FlightValidator()


    def _validate(self, flight_id: str):
        self.validator.validate(flight_id)


    def _parse_dt(self, dt: str):
        return datetime.fromisoformat(dt.replace("Z", "+00:00"))


    def _calculate_total_delay(self, original: str, new: str) -> int:
        o = self._parse_dt(original)
        n = self._parse_dt(new)
        return int((n - o).total_seconds() / 60)


    def _calculate_last_delay_delta(self, total_delay: int, previous_delay: int | None) -> int:
        if previous_delay is None:
            return total_delay  # initial delay
        return total_delay - previous_delay


    def _calculate_sum_positive_diffs(self, history: list[int]) -> int:
        if len(history) < 2:
            return history[0]

        return sum(
            max(0, history[i] - history[i - 1])
            for i in range(1, len(history))
        )


    def _classify(self, total_delay: int, status: str) -> str:
        if status == "Cancelled":
            return "CANCELLED"
        if total_delay >= 60:
            return "AT_RISK_MAJOR_DELAY"
        if total_delay >= 30:
            return "RISK"
        return "STABLE"


    def _generate_why_message(self, classification: str, prev_delay: int | None, total_delay: int, last_delta: int) -> str:
        if prev_delay is None:
            why = f"Initial delay observed as {total_delay} minutes."
        else:
            why = f"Delay changed from {prev_delay} to {total_delay}, increasing by {last_delta} minutes."

        if classification == "AT_RISK_MAJOR_DELAY":
            why += " Major delay threshold (60 minutes) exceeded."

        if classification == "CANCELLED":
            why += " Flight has been cancelled."

        return why
    

    def _build_response(self, flight_id: str, classification: str, last_delta: int,
                        sum_diffs: int, finalETD: str, why: str):

        return {
            flight_id: {
                "classification": classification,
                "lastDelayMin": last_delta,
                "sumPositiveDiffs": sum_diffs,
                "finalETD": finalETD,
                "why": why
            }
        }


    async def get_flight_status(self, flight_id: str):
        
        self._validate(flight_id)

        api_response =  await self.client.get_flight_status(flight_id)
        event = api_response["event"]

        new_dt = event["newDepartureDatetime"]
        orig_dt = event["originalDepartureDatetime"]
        status = event["status"]

        total_delay = self._calculate_total_delay(orig_dt, new_dt)

        previous_state = store.get_state(flight_id)
        previous_delay = previous_state["last_delay"] if previous_state else None

        last_delta = self._calculate_last_delay_delta(total_delay, previous_delay)

        updated_state = store.update_state(
            flight_id=flight_id,
            delay=total_delay,
            event=event
        )

        history = store.get_state(flight_id)["history"]
        sum_positive_diffs = self._calculate_sum_positive_diffs(history)

        classification = self._classify(total_delay, status)

        why = self._generate_why_message(
            classification=classification,
            prev_delay=previous_delay,
            total_delay=total_delay,
            last_delta=last_delta
        )

        return self._build_response(
            flight_id=flight_id,
            classification=classification,
            last_delta=last_delta,
            sum_diffs=sum_positive_diffs,
            finalETD=new_dt,
            why=why
        )