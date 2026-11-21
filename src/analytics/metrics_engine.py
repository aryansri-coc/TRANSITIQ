"""
TransitIQ Analytical Metrics Engine (OLAP Workloads)
Executes optimized SQL aggregations, window functions, and statistical summaries
to power the TransitIQ Command Centre Dashboard.
"""

from typing import Dict, Any, List
import pandas as pd
from src.db.connection import get_engine, execute_query

def get_executive_kpis() -> Dict[str, Any]:
    """
    Computes top-level network operational and commercial KPIs.
    """
    query = """
    SELECT 
        (SELECT COUNT(*) FROM routes WHERE is_active = 1) AS active_routes,
        (SELECT COUNT(*) FROM vehicles WHERE operational_status = 'Active') AS active_vehicles,
        (SELECT COUNT(*) FROM trips) AS total_trips,
        (SELECT COUNT(*) FROM trips WHERE trip_status = 'Completed') AS completed_trips,
        (SELECT COUNT(*) FROM trips WHERE trip_status = 'Delayed') AS delayed_trips,
        (SELECT COUNT(*) FROM trips WHERE trip_status = 'Cancelled') AS cancelled_trips,
        (SELECT COUNT(*) FROM passenger_fares WHERE transaction_status = 'Success') AS total_passengers,
        (SELECT COALESCE(SUM(fare_paid), 0.0) FROM passenger_fares WHERE transaction_status = 'Success') AS total_revenue,
        (SELECT ROUND(AVG(delay_minutes), 1) FROM trips WHERE trip_status IN ('Completed', 'Delayed')) AS network_avg_delay
    """
    rows = execute_query(query)
    kpis = rows[0] if rows else {}

    # Calculate On-time performance %
    completed = kpis.get("completed_trips", 0)
    delayed = kpis.get("delayed_trips", 0)
    operated = completed + delayed
    on_time_pct = round((completed / operated * 100), 1) if operated > 0 else 0.0
    kpis["on_time_performance_pct"] = on_time_pct

    return kpis

def get_route_performance_df() -> pd.DataFrame:
    """
    Returns the analytical summary of route performance from v_route_performance.
    """
    engine = get_engine()
    return pd.read_sql_query("SELECT * FROM v_route_performance ORDER BY total_revenue DESC", engine)

def get_hourly_ridership_df() -> pd.DataFrame:
    """
    Returns hourly ridership trends from v_hourly_ridership.
    """
    engine = get_engine()
    return pd.read_sql_query("SELECT * FROM v_hourly_ridership ORDER BY hour_of_day ASC", engine)

def get_stop_demand_df() -> pd.DataFrame:
    """
    Returns station passenger demand, boardings, and alightings from v_stop_demand_analytics.
    """
    engine = get_engine()
    return pd.read_sql_query("SELECT * FROM v_stop_demand_analytics ORDER BY total_footfall DESC", engine)

def get_fleet_utilization_df() -> pd.DataFrame:
    """
    Returns vehicle fleet health, capacity, and load factor from v_fleet_utilization.
    """
    engine = get_engine()
    return pd.read_sql_query("SELECT * FROM v_fleet_utilization ORDER BY passenger_load_factor_pct DESC", engine)

def get_delay_monitoring_df() -> pd.DataFrame:
    """
    Returns trip punctuality distribution from v_delay_monitoring.
    """
    engine = get_engine()
    return pd.read_sql_query("SELECT * FROM v_delay_monitoring ORDER BY scheduled_departure DESC", engine)

def get_payment_breakdown() -> pd.DataFrame:
    """
    Returns passenger fare distribution by payment method and passenger demographic.
    """
    query = """
    SELECT 
        payment_method,
        passenger_type,
        COUNT(*) AS transaction_count,
        ROUND(SUM(fare_paid), 2) AS total_collected,
        ROUND(AVG(fare_paid), 2) AS avg_ticket_price
    FROM passenger_fares
    WHERE transaction_status = 'Success'
    GROUP BY payment_method, passenger_type
    ORDER BY total_collected DESC
    """
    engine = get_engine()
    return pd.read_sql_query(query, engine)
