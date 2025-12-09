Notes:

Book flights for business travel

Data streams from flight platforms

Data is noisy

Service will track the status of a flight

Service will parse and interpret the data 

Service will inform the user with a descriptive message (delays, etc.)

update

Output format:
{
  "AA123": {
    "classification": "AT_RISK_MAJOR_DELAY", // STABLE | RISK | CANCELLED
    "lastDelayMin": 90,
    "sumPositiveDiffs": 90,
    "finalETD": "2024-10-03T16:30:00Z",
    "why": "Delay progressed from 0 to 15 to 45 to 90 minutes, exceeding the 30-minute threshold"
  }
}

## Events

### Get the next event for a flight

- **Method:** `GET`
- **Endpoint:** `/events`
- **Description:** Retrieves events for a specific flight one by one. Each request for a given `flightId` returns the next event in the sequence. If all events have been returned, it will continuously return the last event.
- **Query Parameters:**
  - `flightId` (required): The ICAO flight ID (e.g., `AA123`).
- **Response:** A JSON object containing the event.

**Response Body Example:**

```json
{
  "event": {
    "flightNumber": "AA123",
    "gate": "A12",
    "newDepartureDatetime": "2024-10-03T15:00:00Z",
    "originalDepartureDatetime": "2024-10-03T15:00:00Z",
    "status": "OnTime", "Possible values: OnTime, Delayed"
    "updateDatetime": "2024-10-03T13:00:00Z"
  }
}
```


## Reset

### Reset event tracking

- **Method:** `POST`
- **Endpoint:** `/reset`
- **Description:** Resets the event counter. If a `flightId` is provided, it resets the counter only for that flight. Otherwise, it resets the counter for all flights.
- **Query Parameters:**
  - `flightId` (optional): The ICAO flight ID to reset (e.g., `AA123`).
- **Response:** A confirmation message.

**Response Body Example (specific flight):**

```json
{
  "message": "Event index reset for flight AA123",
  "flightId": "AA123"
}
```

**Response Body Example (all flights):**

```json
{
  "message": "All flight event indices have been reset",
  "flightsReset": 3
}
```
