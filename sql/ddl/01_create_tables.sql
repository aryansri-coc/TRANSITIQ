-- ============================================================================
-- TransitIQ: Relational Database Schema (DDL)
-- Alignment: Microsoft DP-900 (Azure Data Fundamentals)
-- Normalization: 3NF (Third Normal Form) with strict referential integrity
-- ============================================================================

-- Table 1: STOPS
-- Represents physical transit stations, metro stops, and bus terminals.
CREATE TABLE IF NOT EXISTS stops (
    stop_id INTEGER PRIMARY KEY AUTOINCREMENT,
    stop_code VARCHAR(20) NOT NULL UNIQUE,
    stop_name VARCHAR(100) NOT NULL,
    latitude DECIMAL(9, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,
    zone_id INTEGER NOT NULL DEFAULT 1,
    wheelchair_accessible BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: ROUTES
-- Represents transit lines and corridors across modes.
CREATE TABLE IF NOT EXISTS routes (
    route_id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_code VARCHAR(20) NOT NULL UNIQUE,
    route_name VARCHAR(100) NOT NULL,
    route_type VARCHAR(30) NOT NULL CHECK(route_type IN ('Metro Rail', 'Rapid Bus', 'Express Shuttle', 'Commuter Train')),
    origin_stop_id INTEGER NOT NULL,
    destination_stop_id INTEGER NOT NULL,
    distance_km DECIMAL(6, 2) NOT NULL CHECK(distance_km > 0),
    base_fare DECIMAL(6, 2) NOT NULL CHECK(base_fare >= 0),
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (origin_stop_id) REFERENCES stops(stop_id) ON DELETE RESTRICT,
    FOREIGN KEY (destination_stop_id) REFERENCES stops(stop_id) ON DELETE RESTRICT
);

-- Table 3: ROUTE_SEGMENTS (3NF Junction Table)
-- Resolves the Many-to-Many relationship between Routes and Stops, preserving stop sequences.
CREATE TABLE IF NOT EXISTS route_segments (
    segment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_id INTEGER NOT NULL,
    stop_id INTEGER NOT NULL,
    stop_sequence INTEGER NOT NULL CHECK(stop_sequence > 0),
    distance_from_start_km DECIMAL(6, 2) NOT NULL DEFAULT 0.0,
    est_travel_time_min INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (route_id) REFERENCES routes(route_id) ON DELETE CASCADE,
    FOREIGN KEY (stop_id) REFERENCES stops(stop_id) ON DELETE RESTRICT,
    CONSTRAINT uq_route_stop_sequence UNIQUE (route_id, stop_sequence),
    CONSTRAINT uq_route_stop_pair UNIQUE (route_id, stop_id)
);

-- Table 4: VEHICLES
-- Represents fleet assets (metro rakes, electric buses, commuter cars).
CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_code VARCHAR(20) NOT NULL UNIQUE,
    vehicle_type VARCHAR(30) NOT NULL CHECK(vehicle_type IN ('Metro Rake', 'Electric Bus', 'CNG Standard Bus', 'Double Decker Bus')),
    capacity INTEGER NOT NULL CHECK(capacity > 0),
    fuel_propulsion VARCHAR(30) NOT NULL CHECK(fuel_propulsion IN ('Electric', 'CNG', 'Diesel-Electric Hybrid', 'Hydrogen Cell')),
    operational_status VARCHAR(20) NOT NULL DEFAULT 'Active' CHECK(operational_status IN ('Active', 'Maintenance', 'Depot Reserve', 'Decommissioned')),
    commission_date DATE NOT NULL,
    last_service_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 5: TRIPS
-- Represents scheduled and real-time operational trips executed by vehicles on routes.
CREATE TABLE IF NOT EXISTS trips (
    trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_code VARCHAR(30) NOT NULL UNIQUE,
    route_id INTEGER NOT NULL,
    vehicle_id INTEGER NOT NULL,
    scheduled_departure TIMESTAMP NOT NULL,
    scheduled_arrival TIMESTAMP NOT NULL,
    actual_departure TIMESTAMP,
    actual_arrival TIMESTAMP,
    delay_minutes INTEGER NOT NULL DEFAULT 0,
    trip_status VARCHAR(20) NOT NULL DEFAULT 'Scheduled' CHECK(trip_status IN ('Scheduled', 'In-Transit', 'Completed', 'Delayed', 'Cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (route_id) REFERENCES routes(route_id) ON DELETE RESTRICT,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id) ON DELETE RESTRICT
);

-- Table 6: PASSENGER_FARES (OLTP Transaction Store)
-- Captures atomic ticketing, smartcard taps, and ridership revenue events.
CREATE TABLE IF NOT EXISTS passenger_fares (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_reference VARCHAR(40) NOT NULL UNIQUE,
    trip_id INTEGER NOT NULL,
    origin_stop_id INTEGER NOT NULL,
    destination_stop_id INTEGER NOT NULL,
    passenger_type VARCHAR(20) NOT NULL CHECK(passenger_type IN ('Standard Adult', 'Student', 'Senior Citizen', 'Commuter Passholder')),
    fare_paid DECIMAL(6, 2) NOT NULL CHECK(fare_paid >= 0),
    payment_method VARCHAR(30) NOT NULL CHECK(payment_method IN ('Transit Smartcard', 'Mobile QR / UPI', 'Contactless EMV', 'Ticket Counter')),
    transaction_status VARCHAR(20) NOT NULL DEFAULT 'Success' CHECK(transaction_status IN ('Success', 'Refunded', 'Failed')),
    boarding_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id) ON DELETE RESTRICT,
    FOREIGN KEY (origin_stop_id) REFERENCES stops(stop_id) ON DELETE RESTRICT,
    FOREIGN KEY (destination_stop_id) REFERENCES stops(stop_id) ON DELETE RESTRICT
);

-- ============================================================================
-- PERFORMANCE & ANALYTICAL INDEXES (DP-900 Relational Optimization)
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_routes_type ON routes(route_type);
CREATE INDEX IF NOT EXISTS idx_segments_route_seq ON route_segments(route_id, stop_sequence);
CREATE INDEX IF NOT EXISTS idx_trips_route ON trips(route_id);
CREATE INDEX IF NOT EXISTS idx_trips_vehicle ON trips(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_trips_departure ON trips(scheduled_departure);
CREATE INDEX IF NOT EXISTS idx_trips_status ON trips(trip_status);
CREATE INDEX IF NOT EXISTS idx_fares_trip ON passenger_fares(trip_id);
CREATE INDEX IF NOT EXISTS idx_fares_timestamp ON passenger_fares(boarding_timestamp);
CREATE INDEX IF NOT EXISTS idx_fares_payment ON passenger_fares(payment_method);
