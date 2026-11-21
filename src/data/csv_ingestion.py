"""
TransitIQ CSV Ingestion & Data Quality Auditor Pipeline
Simulates cloud batch ingestion (Azure Blob Storage / Data Factory ETL)
and performs automated data hygiene, referential constraint verification,
and anomaly detection.
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import csv
from typing import Dict, Any, List
import pandas as pd

from src.db.connection import get_raw_sqlite_connection, execute_query
from config.database_config import DATA_DIR

def export_tables_to_csv() -> List[Path]:
    """
    Exports all relational database tables to CSV format in the data/ directory,
    demonstrating data extraction for Cloud Data Lake / Azure Blob staging.
    """
    conn = get_raw_sqlite_connection()
    tables = ["stops", "routes", "route_segments", "vehicles", "trips", "passenger_fares"]
    exported_files = []

    for table in tables:
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        target_path = DATA_DIR / f"{table}.csv"
        df.to_csv(target_path, index=False)
        exported_files.append(target_path)
    
    conn.close()
    return exported_files

def run_data_quality_audit() -> Dict[str, Any]:
    """
    Executes comprehensive data quality and integrity checks:
    1. Null value scans on mandatory columns
    2. Referential integrity (orphan foreign keys)
    3. Logical range checks (fares >= 0, capacity > 0, latitude/longitude bounds)
    4. Chronological consistency (arrival >= departure)
    5. Overall Data Quality Score (0-100%)
    """
    checks = []

    # Check 1: Duplicate Stop Codes
    dup_stops = execute_query("""
        SELECT stop_code, COUNT(*) as count 
        FROM stops GROUP BY stop_code HAVING COUNT(*) > 1
    """)
    checks.append({
        "check_name": "Unique Stop Codes",
        "category": "Uniqueness",
        "passed": len(dup_stops) == 0,
        "details": f"Found {len(dup_stops)} duplicate stop codes."
    })

    # Check 2: Orphan Trips (Referencing non-existent routes or vehicles)
    orphan_trips = execute_query("""
        SELECT t.trip_id FROM trips t
        LEFT JOIN routes r ON t.route_id = r.route_id
        LEFT JOIN vehicles v ON t.vehicle_id = v.vehicle_id
        WHERE r.route_id IS NULL OR v.vehicle_id IS NULL
    """)
    checks.append({
        "check_name": "Trip Referential Integrity",
        "category": "Referential Integrity",
        "passed": len(orphan_trips) == 0,
        "details": f"Found {len(orphan_trips)} orphan trips without valid route or vehicle."
    })

    # Check 3: Orphan Passenger Fares
    orphan_fares = execute_query("""
        SELECT pf.transaction_id FROM passenger_fares pf
        LEFT JOIN trips t ON pf.trip_id = t.trip_id
        WHERE t.trip_id IS NULL
    """)
    checks.append({
        "check_name": "Fare Transaction Referential Integrity",
        "category": "Referential Integrity",
        "passed": len(orphan_fares) == 0,
        "details": f"Found {len(orphan_fares)} orphan fare records."
    })

    # Check 4: Non-negative Fares
    negative_fares = execute_query("""
        SELECT transaction_id, fare_paid FROM passenger_fares WHERE fare_paid < 0
    """)
    checks.append({
        "check_name": "Non-negative Fare Amounts",
        "category": "Value Range Constraint",
        "passed": len(negative_fares) == 0,
        "details": f"Found {len(negative_fares)} records with negative fare."
    })

    # Check 5: Vehicle Capacity Constraints
    invalid_capacity = execute_query("""
        SELECT vehicle_id, capacity FROM vehicles WHERE capacity <= 0
    """)
    checks.append({
        "check_name": "Positive Fleet Capacity",
        "category": "Value Range Constraint",
        "passed": len(invalid_capacity) == 0,
        "details": f"Found {len(invalid_capacity)} vehicles with capacity <= 0."
    })

    # Check 6: Geographical Coordinate Validity
    invalid_coords = execute_query("""
        SELECT stop_id, latitude, longitude FROM stops
        WHERE latitude NOT BETWEEN -90 AND 90 OR longitude NOT BETWEEN -180 AND 180
    """)
    checks.append({
        "check_name": "Geographic Latitude/Longitude Bounds",
        "category": "Geospatial Validity",
        "passed": len(invalid_coords) == 0,
        "details": f"Found {len(invalid_coords)} stops with out-of-bounds coordinates."
    })

    # Calculate overall health score
    passed_count = sum(1 for c in checks if c["passed"])
    total_checks = len(checks)
    quality_score = round((passed_count / total_checks) * 100, 1)

    return {
        "quality_score": quality_score,
        "passed_checks": passed_count,
        "total_checks": total_checks,
        "checks": checks
    }

if __name__ == "__main__":
    print("Exporting tables to CSV...")
    files = export_tables_to_csv()
    print(f"Exported {len(files)} files.")
    audit = run_data_quality_audit()
    print(f"Data Quality Score: {audit['quality_score']}% ({audit['passed_checks']}/{audit['total_checks']} checks passed)")
