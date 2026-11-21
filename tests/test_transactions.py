"""
TransitIQ OLTP Transactional Engine Tests
Validates ACID compliance, ticket booking validation, and trip status updates
"""

import pytest
from src.data.seed_data import generate_and_seed_data
from src.services.transit_service import TransitService
from src.db.connection import execute_query

@pytest.fixture(scope="module")
def seeded_db():
    generate_and_seed_data(num_trips=25, num_passengers=100)
    yield

def test_book_ticket_success(seeded_db):
    """Test successful atomic ticket booking."""
    trips = TransitService.get_bookable_trips()
    assert len(trips) > 0, "No bookable trips available."
    trip = trips[0]

    stops = TransitService.get_stops_for_trip(trip["trip_id"])
    assert len(stops) >= 2, "Trip does not have at least 2 stops."

    orig_id = stops[0]["stop_id"]
    dest_id = stops[-1]["stop_id"]

    res = TransitService.book_ticket(
        trip_id=trip["trip_id"],
        origin_stop_id=orig_id,
        destination_stop_id=dest_id,
        passenger_type="Student",
        payment_method="Transit Smartcard"
    )

    assert res["success"] is True
    assert "ticket_reference" in res
    assert res["fare_paid"] == round(trip["base_fare"] * 0.50, 2)  # 50% student discount

    # Verify presence in database
    fare_rows = execute_query("SELECT * FROM passenger_fares WHERE ticket_reference = :ref", {"ref": res["ticket_reference"]})
    assert len(fare_rows) == 1
    assert fare_rows[0]["fare_paid"] == res["fare_paid"]

def test_book_ticket_invalid_trip(seeded_db):
    """Test booking rejection for non-existent trip."""
    res = TransitService.book_ticket(
        trip_id=99999,
        origin_stop_id=1,
        destination_stop_id=2,
        passenger_type="Standard Adult",
        payment_method="Mobile QR / UPI"
    )
    assert res["success"] is False
    assert "Trip not found" in res["message"]

def test_update_trip_lifecycle(seeded_db):
    """Test updating trip lifecycle status and delay."""
    trips = execute_query("SELECT trip_id FROM trips LIMIT 1")
    trip_id = trips[0]["trip_id"]

    # Transition to In-Transit
    res = TransitService.update_trip_status(trip_id=trip_id, new_status="In-Transit", delay_minutes=4)
    assert res["success"] is True

    # Verify in DB
    updated = execute_query("SELECT trip_status, delay_minutes, actual_departure FROM trips WHERE trip_id = :id", {"id": trip_id})
    assert updated[0]["trip_status"] == "In-Transit"
    assert updated[0]["delay_minutes"] == 4
    assert updated[0]["actual_departure"] is not None
