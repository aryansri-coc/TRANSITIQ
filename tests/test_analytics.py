"""
TransitIQ OLAP Analytical Metrics Tests
Validates View Calculations, KPI Accuracy, and Data Integrity
"""

import pytest
from src.data.seed_data import generate_and_seed_data
from src.analytics.metrics_engine import (
    get_executive_kpis,
    get_route_performance_df,
    get_hourly_ridership_df,
    get_stop_demand_df,
    get_fleet_utilization_df
)
from src.data.csv_ingestion import run_data_quality_audit

@pytest.fixture(scope="module")
def seeded_db():
    generate_and_seed_data(num_trips=40, num_passengers=250)
    yield

def test_executive_kpis(seeded_db):
    """Validate executive KPI computations."""
    kpis = get_executive_kpis()
    assert kpis["active_routes"] > 0
    assert kpis["active_vehicles"] > 0
    assert kpis["total_trips"] > 0
    assert kpis["total_passengers"] > 0
    assert kpis["total_revenue"] > 0
    assert 0.0 <= kpis["on_time_performance_pct"] <= 100.0

def test_route_performance_view(seeded_db):
    """Validate route performance view aggregations."""
    df = get_route_performance_df()
    assert not df.empty
    assert "route_code" in df.columns
    assert "total_revenue" in df.columns
    assert "total_passengers" in df.columns
    # All revenues should be non-negative
    assert (df["total_revenue"] >= 0).all()

def test_stop_demand_view(seeded_db):
    """Validate station demand calculations."""
    df = get_stop_demand_df()
    assert not df.empty
    assert "total_boardings" in df.columns
    assert "total_alightings" in df.columns
    assert "total_footfall" in df.columns
    assert (df["total_footfall"] == df["total_boardings"] + df["total_alightings"]).all()

def test_data_quality_audit(seeded_db):
    """Validate automated data hygiene audit."""
    audit = run_data_quality_audit()
    assert audit["quality_score"] == 100.0
    assert audit["passed_checks"] == audit["total_checks"]
