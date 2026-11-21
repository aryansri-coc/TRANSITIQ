"""
TransitIQ Relational Schema & Data Integrity Unit Tests
Validates Table Creation, Foreign Key Constraints, and 3NF Normalization
"""

import pytest
import sqlite3
from src.db.connection import get_raw_sqlite_connection, initialize_database, execute_query

@pytest.fixture(scope="module")
def setup_db():
    initialize_database(reset=True)
    yield
    # teardown if needed

def test_tables_created(setup_db):
    """Verify that all six core relational tables exist."""
    tables = execute_query("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
    """)
    table_names = [t["name"] for t in tables]
    expected_tables = ["stops", "routes", "route_segments", "vehicles", "trips", "passenger_fares"]
    for expected in expected_tables:
        assert expected in table_names, f"Table {expected} was not created."

def test_views_created(setup_db):
    """Verify that all analytical OLAP views exist."""
    views = execute_query("""
        SELECT name FROM sqlite_master 
        WHERE type='view'
    """)
    view_names = [v["name"] for v in views]
    expected_views = [
        "v_route_performance",
        "v_hourly_ridership",
        "v_stop_demand_analytics",
        "v_fleet_utilization",
        "v_delay_monitoring"
    ]
    for expected in expected_views:
        assert expected in view_names, f"View {expected} was not created."

def test_foreign_key_enforcement(setup_db):
    """Verify foreign key constraint rejects orphan routes."""
    conn = get_raw_sqlite_connection()
    cursor = conn.cursor()
    with pytest.raises(sqlite3.IntegrityError):
        # Insert route pointing to non-existent stops (999, 998)
        cursor.execute("""
            INSERT INTO routes (route_code, route_name, route_type, origin_stop_id, destination_stop_id, distance_km, base_fare)
            VALUES ('INV-01', 'Invalid Route', 'Rapid Bus', 999, 998, 12.0, 20.0)
        """)
        conn.commit()
    conn.close()

def test_check_constraints(setup_db):
    """Verify check constraints prevent invalid route types or negative distance."""
    conn = get_raw_sqlite_connection()
    cursor = conn.cursor()
    # 1. Invalid Route Type
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("""
            INSERT INTO routes (route_code, route_name, route_type, origin_stop_id, destination_stop_id, distance_km, base_fare)
            VALUES ('INV-02', 'Invalid Type', 'Submarine', 1, 2, 10.0, 20.0)
        """)
        conn.commit()

    # 2. Negative Distance
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("""
            INSERT INTO routes (route_code, route_name, route_type, origin_stop_id, destination_stop_id, distance_km, base_fare)
            VALUES ('INV-03', 'Negative Dist', 'Rapid Bus', 1, 2, -15.0, 20.0)
        """)
        conn.commit()
    conn.close()

def test_3nf_junction_uniqueness(setup_db):
    """Verify that duplicate stop sequences or stop pairs on a route are rejected."""
    conn = get_raw_sqlite_connection()
    cursor = conn.cursor()
    # Insert test stops
    cursor.execute("INSERT INTO stops (stop_code, stop_name, latitude, longitude) VALUES ('T-S1', 'Test S1', 28.0, 77.0)")
    s1_id = cursor.lastrowid
    cursor.execute("INSERT INTO stops (stop_code, stop_name, latitude, longitude) VALUES ('T-S2', 'Test S2', 28.1, 77.1)")
    s2_id = cursor.lastrowid

    # Insert test route
    cursor.execute(f"INSERT INTO routes (route_code, route_name, route_type, origin_stop_id, destination_stop_id, distance_km, base_fare) VALUES ('T-R1', 'Test Route', 'Rapid Bus', {s1_id}, {s2_id}, 10.0, 25.0)")
    r1_id = cursor.lastrowid

    # Insert valid segment
    cursor.execute(f"INSERT INTO route_segments (route_id, stop_id, stop_sequence, distance_from_start_km) VALUES ({r1_id}, {s1_id}, 1, 0.0)")

    # Insert duplicate sequence 1 for same route -> should fail
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute(f"INSERT INTO route_segments (route_id, stop_id, stop_sequence, distance_from_start_km) VALUES ({r1_id}, {s2_id}, 1, 5.0)")
        conn.commit()

    conn.close()
