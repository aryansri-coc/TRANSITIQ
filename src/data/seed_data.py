"""
TransitIQ Synthetic Data Generation Module
Generates a realistic, multi-modal metropolitan transit network with:
- 12 Stations & Terminals
- 6 Multi-Modal Transit Routes (Metro, BRT, Express, Commuter)
- 42 Route Segments (preserving stop order & distance)
- 16 Modern Vehicles (Metro trains, EV buses, CNG buses)
- 150+ Trips across peak and off-peak hours
- 2,000+ Passenger ticketing & boarding transactions
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import random
from datetime import datetime, timedelta, date
from typing import List, Dict, Any

from src.db.connection import get_raw_sqlite_connection, initialize_database

def generate_and_seed_data(num_trips: int = 160, num_passengers: int = 2200):
    """
    Populates the database with realistic metropolitan transit operations data.
    """
    initialize_database(reset=True)
    conn = get_raw_sqlite_connection()
    cursor = conn.cursor()

    print("Seeding Stops...")
    stops_data = [
        ("ST-01", "Central Metro Grand Station", 28.6328, 77.2197, 1, 1),
        ("ST-02", "Cyber City Tech Park", 28.4950, 77.0895, 2, 1),
        ("ST-03", "National University North Campus", 28.6853, 77.2112, 1, 1),
        ("ST-04", "Terminal 3 International Airport", 28.5562, 77.1000, 3, 1),
        ("ST-05", "Harbor Gate Waterfront", 28.6139, 77.2090, 1, 1),
        ("ST-06", "Northern Suburb Interchange", 28.7200, 77.1500, 2, 1),
        ("ST-07", "Southern Express Terminal", 28.4500, 77.0500, 3, 1),
        ("ST-08", "East River City Market", 28.6200, 77.2800, 2, 1),
        ("ST-09", "Heritage Old Town Plaza", 28.6506, 77.2303, 1, 0),
        ("ST-10", "Innovation Hub & Biotech Park", 28.5200, 77.2500, 2, 1),
        ("ST-11", "Metropolitan Apex Hospital", 28.5700, 77.2200, 1, 1),
        ("ST-12", "West End Industrial Junction", 28.6400, 77.1200, 2, 1),
    ]
    cursor.executemany("""
        INSERT INTO stops (stop_code, stop_name, latitude, longitude, zone_id, wheelchair_accessible)
        VALUES (?, ?, ?, ?, ?, ?)
    """, stops_data)

    print("Seeding Routes...")
    routes_data = [
        ("M-RED", "Red Line Metro Expressway", "Metro Rail", 1, 4, 24.5, 40.0, 1),
        ("M-BLUE", "Blue Line Metro Link", "Metro Rail", 3, 2, 32.0, 50.0, 1),
        ("BRT-101", "North-South Rapid Transit", "Rapid Bus", 6, 7, 38.0, 30.0, 1),
        ("BRT-102", "Heritage to Medical Corridor", "Rapid Bus", 9, 11, 16.5, 20.0, 1),
        ("EXP-500", "Silicon Express Shuttle", "Express Shuttle", 10, 2, 18.2, 35.0, 1),
        ("CR-10", "Regional Commuter Line", "Commuter Train", 6, 1, 28.0, 25.0, 1),
    ]
    cursor.executemany("""
        INSERT INTO routes (route_code, route_name, route_type, origin_stop_id, destination_stop_id, distance_km, base_fare, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, routes_data)

    print("Seeding Route Segments (3NF Junctions)...")
    # Define ordered sequences of stops for each route
    route_stop_sequences = {
        1: [1, 5, 11, 4],            # M-RED: Central -> Harbor -> Hospital -> Airport
        2: [3, 9, 1, 10, 2],         # M-BLUE: University -> Old Town -> Central -> Innovation -> Cyber City
        3: [6, 12, 1, 11, 7],        # BRT-101: North -> West End -> Central -> Hospital -> South
        4: [9, 1, 5, 8, 11],         # BRT-102: Old Town -> Central -> Harbor -> East River -> Hospital
        5: [10, 5, 2],               # EXP-500: Innovation -> Harbor -> Cyber City
        6: [6, 3, 9, 1],             # CR-10: North -> University -> Old Town -> Central
    }

    segments_data = []
    for r_id, stop_list in route_stop_sequences.items():
        cumulative_dist = 0.0
        cumulative_time = 0
        for seq, stop_id in enumerate(stop_list, start=1):
            if seq > 1:
                cumulative_dist += round(random.uniform(3.5, 7.5), 1)
                cumulative_time += random.randint(8, 16)
            segments_data.append((r_id, stop_id, seq, round(cumulative_dist, 1), cumulative_time))

    cursor.executemany("""
        INSERT INTO route_segments (route_id, stop_id, stop_sequence, distance_from_start_km, est_travel_time_min)
        VALUES (?, ?, ?, ?, ?)
    """, segments_data)

    print("Seeding Vehicle Fleet...")
    vehicles_data = [
        ("METRO-01", "Metro Rake", 800, "Electric", "Active", "2023-01-15", "2026-10-10"),
        ("METRO-02", "Metro Rake", 800, "Electric", "Active", "2023-03-20", "2026-10-12"),
        ("METRO-03", "Metro Rake", 800, "Electric", "Active", "2024-05-11", "2026-11-01"),
        ("METRO-04", "Metro Rake", 800, "Electric", "Maintenance", "2022-08-01", "2026-11-15"),
        ("EBUS-101", "Electric Bus", 75, "Electric", "Active", "2024-02-10", "2026-11-05"),
        ("EBUS-102", "Electric Bus", 75, "Electric", "Active", "2024-02-14", "2026-11-06"),
        ("EBUS-103", "Electric Bus", 75, "Electric", "Active", "2024-06-22", "2026-10-28"),
        ("EBUS-104", "Electric Bus", 75, "Electric", "Active", "2025-01-10", "2026-11-08"),
        ("CNG-201", "CNG Standard Bus", 55, "CNG", "Active", "2022-04-12", "2026-10-15"),
        ("CNG-202", "CNG Standard Bus", 55, "CNG", "Active", "2022-07-19", "2026-10-20"),
        ("CNG-203", "CNG Standard Bus", 55, "CNG", "Active", "2023-09-05", "2026-11-02"),
        ("CNG-204", "CNG Standard Bus", 55, "CNG", "Depot Reserve", "2021-11-30", "2026-09-15"),
        ("DDECK-301", "Double Decker Bus", 90, "Electric", "Active", "2025-03-15", "2026-10-25"),
        ("DDECK-302", "Double Decker Bus", 90, "Electric", "Active", "2025-03-18", "2026-11-12"),
        ("HYD-401", "Electric Bus", 65, "Hydrogen Cell", "Active", "2025-08-10", "2026-11-04"),
        ("COMM-501", "Metro Rake", 650, "Electric", "Active", "2023-10-15", "2026-10-30"),
    ]
    cursor.executemany("""
        INSERT INTO vehicles (vehicle_code, vehicle_type, capacity, fuel_propulsion, operational_status, commission_date, last_service_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, vehicles_data)

    print("Generating Operational Trips...")
    base_time = datetime.now() - timedelta(days=5)
    trips_data = []
    trip_id_counter = 1

    # Map route type to appropriate vehicle IDs
    metro_vehicles = [1, 2, 3, 16]
    bus_vehicles = [5, 6, 7, 8, 9, 10, 11, 13, 14, 15]

    for day in range(5):
        day_date = base_time + timedelta(days=day)
        # Service runs from 06:00 to 22:00
        for hour in range(6, 23):
            # Peak hours have higher frequency
            is_peak = hour in [8, 9, 10, 17, 18, 19]
            trips_in_hour = 2 if is_peak else 1

            for _ in range(trips_in_hour):
                for route_id in range(1, 7):
                    # Select vehicle type matching route
                    v_id = random.choice(metro_vehicles) if route_id in (1, 2, 6) else random.choice(bus_vehicles)
                    minute = random.randint(0, 55)
                    sched_dep = day_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    trip_duration = timedelta(minutes=random.randint(25, 65))
                    sched_arr = sched_dep + trip_duration

                    # Determine status and delay
                    rand_val = random.random()
                    if rand_val < 0.03:
                        status = "Cancelled"
                        act_dep = None
                        act_arr = None
                        delay = 0
                    elif rand_val < 0.18:
                        # Currently scheduled for upcoming service
                        status = "Scheduled"
                        act_dep = None
                        act_arr = None
                        delay = 0
                    elif rand_val < 0.30:
                        # Active in-transit right now
                        status = "In-Transit"
                        delay = random.randint(0, 8)
                        act_dep = sched_dep + timedelta(minutes=delay)
                        act_arr = None
                    elif rand_val < 0.45:
                        # Delayed
                        status = "Delayed"
                        delay = random.randint(6, 25)
                        act_dep = sched_dep + timedelta(minutes=delay)
                        act_arr = sched_arr + timedelta(minutes=delay + random.randint(-2, 5))
                    else:
                        # Completed on-time / minor
                        status = "Completed"
                        delay = random.randint(-2, 4)
                        act_dep = sched_dep + timedelta(minutes=max(0, delay))
                        act_arr = sched_arr + timedelta(minutes=delay)

                    trip_code = f"TRIP-{day+1:02d}-{route_id}-{trip_id_counter:04d}"
                    trips_data.append((
                        trip_code, route_id, v_id,
                        sched_dep.strftime("%Y-%m-%d %H:%M:%S"),
                        sched_arr.strftime("%Y-%m-%d %H:%M:%S"),
                        act_dep.strftime("%Y-%m-%d %H:%M:%S") if act_dep else None,
                        act_arr.strftime("%Y-%m-%d %H:%M:%S") if act_arr else None,
                        delay,
                        status
                    ))
                    trip_id_counter += 1

    # Cap to requested number of trips
    selected_trips = trips_data[:num_trips]
    cursor.executemany("""
        INSERT INTO trips (trip_code, route_id, vehicle_id, scheduled_departure, scheduled_arrival, actual_departure, actual_arrival, delay_minutes, trip_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, selected_trips)

    print("Generating Passenger Fares & Ticketing Transactions...")
    passenger_types = ["Standard Adult", "Student", "Senior Citizen", "Commuter Passholder"]
    passenger_weights = [0.55, 0.20, 0.10, 0.15]

    payment_methods = ["Transit Smartcard", "Mobile QR / UPI", "Contactless EMV", "Ticket Counter"]
    payment_weights = [0.45, 0.35, 0.15, 0.05]

    # Query valid trips and their route details
    cursor.execute("""
        SELECT t.trip_id, t.route_id, t.scheduled_departure, r.base_fare
        FROM trips t
        JOIN routes r ON t.route_id = r.route_id
        WHERE t.trip_status IN ('Completed', 'Delayed', 'In-Transit', 'Scheduled')
    """)
    valid_trips = cursor.fetchall()

    fares_data = []
    ticket_counter = 1

    for _ in range(num_passengers):
        trip_id, route_id, sched_dep_str, base_fare = random.choice(valid_trips)
        sched_dep = datetime.strptime(sched_dep_str, "%Y-%m-%d %H:%M:%S")
        
        # Boarding happens within 10 minutes of departure
        boarding_time = sched_dep + timedelta(minutes=random.randint(-10, 2))
        
        stops_in_route = route_stop_sequences[route_id]
        if len(stops_in_route) >= 2:
            orig_idx = random.randint(0, len(stops_in_route) - 2)
            dest_idx = random.randint(orig_idx + 1, len(stops_in_route) - 1)
            orig_stop = stops_in_route[orig_idx]
            dest_stop = stops_in_route[dest_idx]
        else:
            orig_stop = stops_in_route[0]
            dest_stop = stops_in_route[-1]

        p_type = random.choices(passenger_types, weights=passenger_weights)[0]
        pay_method = random.choices(payment_methods, weights=payment_weights)[0]

        # Calculate discounted fare
        fare_factor = 1.0
        if p_type == "Student":
            fare_factor = 0.50
        elif p_type == "Senior Citizen":
            fare_factor = 0.40
        elif p_type == "Commuter Passholder":
            fare_factor = 0.70

        fare_paid = round(base_fare * fare_factor, 2)
        ticket_ref = f"TKT-{boarding_time.strftime('%y%m%d')}-{ticket_counter:06d}"
        ticket_counter += 1

        fares_data.append((
            ticket_ref, trip_id, orig_stop, dest_stop,
            p_type, fare_paid, pay_method, "Success",
            boarding_time.strftime("%Y-%m-%d %H:%M:%S")
        ))

    cursor.executemany("""
        INSERT INTO passenger_fares (
            ticket_reference, trip_id, origin_stop_id, destination_stop_id,
            passenger_type, fare_paid, payment_method, transaction_status, boarding_timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, fares_data)

    conn.commit()
    conn.close()
    print(f"Data seeding complete! Inserted {len(stops_data)} stops, {len(routes_data)} routes, {len(segments_data)} segments, {len(vehicles_data)} vehicles, {len(selected_trips)} trips, and {len(fares_data)} passenger transactions.")

if __name__ == "__main__":
    generate_and_seed_data()
