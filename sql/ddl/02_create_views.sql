-- ============================================================================
-- TransitIQ: Analytical Views (OLAP Workload Layer)
-- Alignment: Microsoft DP-900 (Analytical queries, aggregations, windowing)
-- ============================================================================

-- View 1: Route Performance & Efficiency Summary
CREATE VIEW IF NOT EXISTS v_route_performance AS
SELECT 
    r.route_id,
    r.route_code,
    r.route_name,
    r.route_type,
    r.distance_km,
    COUNT(DISTINCT t.trip_id) AS total_trips,
    SUM(CASE WHEN t.trip_status = 'Completed' THEN 1 ELSE 0 END) AS completed_trips,
    SUM(CASE WHEN t.trip_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_trips,
    ROUND(AVG(CASE WHEN t.trip_status = 'Completed' THEN t.delay_minutes ELSE NULL END), 2) AS avg_delay_minutes,
    ROUND(
        100.0 * SUM(CASE WHEN t.trip_status = 'Completed' AND t.delay_minutes <= 5 THEN 1 ELSE 0 END) / 
        NULLIF(SUM(CASE WHEN t.trip_status IN ('Completed', 'Delayed') THEN 1 ELSE 0 END), 0), 
        2
    ) AS on_time_percentage,
    COUNT(pf.transaction_id) AS total_passengers,
    COALESCE(SUM(pf.fare_paid), 0.0) AS total_revenue
FROM routes r
LEFT JOIN trips t ON r.route_id = t.route_id
LEFT JOIN passenger_fares pf ON t.trip_id = pf.trip_id AND pf.transaction_status = 'Success'
GROUP BY r.route_id, r.route_code, r.route_name, r.route_type, r.distance_km;

-- View 2: Hourly Passenger Ridership and Peak Load Distribution
CREATE VIEW IF NOT EXISTS v_hourly_ridership AS
SELECT 
    strftime('%H', pf.boarding_timestamp) AS hour_of_day,
    r.route_type,
    COUNT(pf.transaction_id) AS passenger_count,
    ROUND(SUM(pf.fare_paid), 2) AS hourly_revenue,
    CASE 
        WHEN strftime('%H', pf.boarding_timestamp) IN ('08', '09', '10', '17', '18', '19') THEN 'Peak Rush Hour'
        WHEN strftime('%H', pf.boarding_timestamp) BETWEEN '11' AND '16' THEN 'Midday Normal'
        WHEN strftime('%H', pf.boarding_timestamp) BETWEEN '20' AND '23' THEN 'Late Evening'
        ELSE 'Early Morning / Night'
    END AS service_period
FROM passenger_fares pf
JOIN trips t ON pf.trip_id = t.trip_id
JOIN routes r ON t.route_id = r.route_id
WHERE pf.transaction_status = 'Success'
GROUP BY hour_of_day, r.route_type, service_period;

-- View 3: Stop-Level Passenger Demand Analytics (Hub Utilization)
CREATE VIEW IF NOT EXISTS v_stop_demand_analytics AS
SELECT 
    s.stop_id,
    s.stop_code,
    s.stop_name,
    s.zone_id,
    s.latitude,
    s.longitude,
    COALESCE(b.boardings, 0) AS total_boardings,
    COALESCE(a.alightings, 0) AS total_alightings,
    COALESCE(b.boardings, 0) + COALESCE(a.alightings, 0) AS total_footfall
FROM stops s
LEFT JOIN (
    SELECT origin_stop_id, COUNT(*) AS boardings 
    FROM passenger_fares 
    WHERE transaction_status = 'Success' 
    GROUP BY origin_stop_id
) b ON s.stop_id = b.origin_stop_id
LEFT JOIN (
    SELECT destination_stop_id, COUNT(*) AS alightings 
    FROM passenger_fares 
    WHERE transaction_status = 'Success' 
    GROUP BY destination_stop_id
) a ON s.stop_id = a.destination_stop_id;

-- View 4: Vehicle Fleet Health, Capacity & Utilization
CREATE VIEW IF NOT EXISTS v_fleet_utilization AS
SELECT 
    v.vehicle_id,
    v.vehicle_code,
    v.vehicle_type,
    v.capacity,
    v.fuel_propulsion,
    v.operational_status,
    COUNT(t.trip_id) AS total_trips_assigned,
    SUM(CASE WHEN t.trip_status = 'Completed' THEN 1 ELSE 0 END) AS trips_completed,
    COALESCE(SUM(r.distance_km), 0) AS total_km_operated,
    COUNT(pf.transaction_id) AS total_passengers_served,
    ROUND(
        100.0 * COUNT(pf.transaction_id) / 
        NULLIF(SUM(CASE WHEN t.trip_status = 'Completed' THEN v.capacity ELSE 0 END), 0), 
        2
    ) AS passenger_load_factor_pct
FROM vehicles v
LEFT JOIN trips t ON v.vehicle_id = t.vehicle_id
LEFT JOIN routes r ON t.route_id = r.route_id
LEFT JOIN passenger_fares pf ON t.trip_id = pf.trip_id AND pf.transaction_status = 'Success'
GROUP BY v.vehicle_id, v.vehicle_code, v.vehicle_type, v.capacity, v.fuel_propulsion, v.operational_status;

-- View 5: Punctuality and Delay Risk Categorization
CREATE VIEW IF NOT EXISTS v_delay_monitoring AS
SELECT 
    t.trip_id,
    t.trip_code,
    r.route_code,
    r.route_name,
    v.vehicle_code,
    t.scheduled_departure,
    t.actual_departure,
    t.delay_minutes,
    t.trip_status,
    CASE 
        WHEN t.trip_status = 'Cancelled' THEN 'Cancelled'
        WHEN t.delay_minutes <= 0 THEN 'Early / On-Time'
        WHEN t.delay_minutes BETWEEN 1 AND 5 THEN 'Acceptable (1-5m)'
        WHEN t.delay_minutes BETWEEN 6 AND 15 THEN 'Moderate Delay (6-15m)'
        ELSE 'Severe Delay (>15m)'
    END AS delay_category
FROM trips t
JOIN routes r ON t.route_id = r.route_id
JOIN vehicles v ON t.vehicle_id = v.vehicle_id;
