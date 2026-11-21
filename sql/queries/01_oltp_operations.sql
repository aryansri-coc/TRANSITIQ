-- ============================================================================
-- TransitIQ: OLTP Operations (Online Transaction Processing)
-- Alignment: Microsoft DP-900 (Relational Data & Transactional Workloads)
-- Characteristics: High frequency, low latency, atomic writes, ACID compliance
-- ============================================================================

-- ----------------------------------------------------------------------------
-- OLTP Scenario 1: Atomic Passenger Ticket Issuance (ACID Transaction)
-- Demonstrates atomic write with foreign key integrity and check constraints.
-- ----------------------------------------------------------------------------
BEGIN TRANSACTION;

-- Step A: Validate capacity and insert ticketing record
INSERT INTO passenger_fares (
    ticket_reference,
    trip_id,
    origin_stop_id,
    destination_stop_id,
    passenger_type,
    fare_paid,
    payment_method,
    transaction_status,
    boarding_timestamp
)
VALUES (
    'TKT-DEMO-20261120-0099',
    1,   -- Trip ID
    1,   -- Central Metro Grand Station
    4,   -- Airport Terminal 3
    'Standard Adult',
    40.00,
    'Transit Smartcard',
    'Success',
    CURRENT_TIMESTAMP
);

COMMIT;

-- ----------------------------------------------------------------------------
-- OLTP Scenario 2: Operational Dispatch Trip Status Transition
-- Transitions trip from 'Scheduled' to 'In-Transit' with actual timestamp.
-- ----------------------------------------------------------------------------
BEGIN TRANSACTION;

UPDATE trips
SET 
    trip_status = 'In-Transit',
    actual_departure = CURRENT_TIMESTAMP,
    delay_minutes = 3
WHERE trip_id = 5
  AND trip_status = 'Scheduled';

COMMIT;

-- ----------------------------------------------------------------------------
-- OLTP Scenario 3: Real-Time Fleet Asset Status Toggle (Maintenance Dispatch)
-- ----------------------------------------------------------------------------
BEGIN TRANSACTION;

UPDATE vehicles
SET 
    operational_status = 'Maintenance',
    last_service_date = CURRENT_DATE
WHERE vehicle_code = 'EBUS-102';

COMMIT;
