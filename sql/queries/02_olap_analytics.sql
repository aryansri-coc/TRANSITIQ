-- ============================================================================
-- TransitIQ: OLAP Analytics (Online Analytical Processing)
-- Alignment: Microsoft DP-900 (Analytical Workloads, Aggregations, CTEs, Windowing)
-- Characteristics: Complex multi-table joins, aggregations, trend analysis
-- ============================================================================

-- ----------------------------------------------------------------------------
-- OLAP Query 1: Multi-Stage Route Profitability & Passenger Load Factor
-- Uses Common Table Expressions (CTEs) to isolate operational costs vs revenue.
-- ----------------------------------------------------------------------------
WITH RouteTripStats AS (
    SELECT 
        r.route_id,
        r.route_code,
        r.route_name,
        r.route_type,
        r.distance_km,
        COUNT(DISTINCT t.trip_id) AS total_trips,
        SUM(CASE WHEN t.trip_status = 'Completed' THEN 1 ELSE 0 END) AS completed_trips
    FROM routes r
    LEFT JOIN trips t ON r.route_id = t.route_id
    GROUP BY r.route_id, r.route_code, r.route_name, r.route_type, r.distance_km
),
RouteRidershipStats AS (
    SELECT 
        t.route_id,
        COUNT(pf.transaction_id) AS total_riders,
        COALESCE(SUM(pf.fare_paid), 0.0) AS total_revenue,
        ROUND(AVG(pf.fare_paid), 2) AS avg_fare_per_rider
    FROM trips t
    JOIN passenger_fares pf ON t.trip_id = pf.trip_id
    WHERE pf.transaction_status = 'Success'
    GROUP BY t.route_id
)
SELECT 
    ts.route_code,
    ts.route_name,
    ts.route_type,
    ts.distance_km,
    ts.completed_trips,
    COALESCE(rs.total_riders, 0) AS total_riders,
    COALESCE(rs.total_revenue, 0.0) AS total_revenue,
    ROUND(COALESCE(rs.total_revenue, 0.0) / NULLIF(ts.distance_km * ts.completed_trips, 0), 2) AS revenue_per_vehicle_km
FROM RouteTripStats ts
LEFT JOIN RouteRidershipStats rs ON ts.route_id = rs.route_id
ORDER BY total_revenue DESC;

-- ----------------------------------------------------------------------------
-- OLAP Query 2: Peak vs Off-Peak Hourly Ridership Demand Curve
-- Aggregates passenger volumes into operational service windows.
-- ----------------------------------------------------------------------------
SELECT 
    strftime('%H', pf.boarding_timestamp) AS hour_of_day,
    CASE 
        WHEN strftime('%H', pf.boarding_timestamp) IN ('08', '09', '10', '17', '18', '19') THEN 'Peak Rush Hour'
        WHEN strftime('%H', pf.boarding_timestamp) BETWEEN '11' AND '16' THEN 'Midday Regular'
        ELSE 'Off-Peak / Night'
    END AS service_period,
    COUNT(pf.transaction_id) AS ridership_count,
    ROUND(SUM(pf.fare_paid), 2) AS period_revenue,
    ROUND(AVG(pf.fare_paid), 2) AS avg_fare
FROM passenger_fares pf
WHERE pf.transaction_status = 'Success'
GROUP BY hour_of_day, service_period
ORDER BY hour_of_day ASC;

-- ----------------------------------------------------------------------------
-- OLAP Query 3: Window Function - Cumulative Daily Revenue Trend
-- Demonstrates SQL analytical window function SUM(...) OVER(...) partitioned by date.
-- ----------------------------------------------------------------------------
SELECT 
    DATE(pf.boarding_timestamp) AS travel_date,
    strftime('%H', pf.boarding_timestamp) AS travel_hour,
    COUNT(pf.transaction_id) AS hourly_passengers,
    ROUND(SUM(pf.fare_paid), 2) AS hourly_revenue,
    ROUND(SUM(SUM(pf.fare_paid)) OVER (
        PARTITION BY DATE(pf.boarding_timestamp) 
        ORDER BY strftime('%H', pf.boarding_timestamp)
    ), 2) AS cumulative_daily_revenue
FROM passenger_fares pf
WHERE pf.transaction_status = 'Success'
GROUP BY travel_date, travel_hour
ORDER BY travel_date DESC, travel_hour ASC;
