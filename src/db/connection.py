"""
TransitIQ Database Connection & Execution Engine
Provides unified connection pooling, script execution, and transactional wrappers
supporting both local SQLite and Azure SQL Database.
"""

import sqlite3
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from config.database_config import get_connection_string, get_sqlite_path, DB_DIALECT, BASE_DIR

_engine: Optional[Engine] = None

def get_engine() -> Engine:
    """Returns singleton SQLAlchemy Engine."""
    global _engine
    if _engine is None:
        conn_str = get_connection_string()
        if "sqlite" in conn_str:
            _engine = create_engine(conn_str, connect_args={"check_same_thread": False})
        else:
            _engine = create_engine(conn_str, pool_pre_ping=True, pool_size=10)
    return _engine

def get_raw_sqlite_connection() -> sqlite3.Connection:
    """Returns a native sqlite3 connection with Row factory enabled."""
    db_path = get_sqlite_path()
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def execute_query(query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Executes a SELECT query and returns a list of dictionaries.
    """
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(query), params or {})
        keys = result.keys()
        return [dict(zip(keys, row)) for row in result.fetchall()]

def execute_statement(statement: str, params: Optional[Dict[str, Any]] = None) -> int:
    """
    Executes an INSERT, UPDATE, or DELETE statement inside a transaction.
    Returns rows affected.
    """
    engine = get_engine()
    with engine.begin() as conn:
        result = conn.execute(text(statement), params or {})
        return result.rowcount

def execute_script(script_text: str):
    """
    Executes a multi-statement SQL script.
    """
    if DB_DIALECT == "sqlite":
        conn = get_raw_sqlite_connection()
        try:
            conn.executescript(script_text)
            conn.commit()
        finally:
            conn.close()
    else:
        engine = get_engine()
        with engine.begin() as conn:
            # For SQL Server/T-SQL, split by GO or execute directly
            for statement in script_text.split(";"):
                stmt = statement.strip()
                if stmt:
                    conn.execute(text(stmt))

def initialize_database(reset: bool = False):
    """
    Initializes tables, views, and indexes.
    If reset is True, drops existing views and tables in reverse dependency order,
    guaranteeing clean re-initialization without file lock errors on Windows.
    """
    global _engine
    if _engine is not None:
        _engine.dispose()
        _engine = None

    if reset:
        if DB_DIALECT == "sqlite":
            conn = get_raw_sqlite_connection()
            try:
                cursor = conn.cursor()
                # Disable foreign keys temporarily for clean cascade drop
                cursor.execute("PRAGMA foreign_keys = OFF;")
                views = [
                    "v_route_performance", "v_hourly_ridership", "v_stop_demand_analytics",
                    "v_fleet_utilization", "v_delay_monitoring"
                ]
                for v in views:
                    cursor.execute(f"DROP VIEW IF EXISTS {v}")
                
                tables = [
                    "passenger_fares", "trips", "route_segments", "vehicles", "routes", "stops"
                ]
                for t in tables:
                    cursor.execute(f"DROP TABLE IF EXISTS {t}")
                conn.commit()
                cursor.execute("PRAGMA foreign_keys = ON;")
            finally:
                conn.close()
        else:
            engine = get_engine()
            with engine.begin() as conn:
                for v in ["v_route_performance", "v_hourly_ridership", "v_stop_demand_analytics", "v_fleet_utilization", "v_delay_monitoring"]:
                    conn.execute(text(f"DROP VIEW IF EXISTS {v}"))
                for t in ["passenger_fares", "trips", "route_segments", "vehicles", "routes", "stops"]:
                    conn.execute(text(f"DROP TABLE IF EXISTS {t}"))

    ddl_dir = BASE_DIR / "sql" / "ddl"
    tables_sql = (ddl_dir / "01_create_tables.sql").read_text(encoding="utf-8")
    views_sql = (ddl_dir / "02_create_views.sql").read_text(encoding="utf-8")

    execute_script(tables_sql)
    execute_script(views_sql)

if __name__ == "__main__":
    print(f"Initializing TransitIQ database in dialect: {DB_DIALECT}")
    initialize_database(reset=True)
    print("Database initialized successfully.")
