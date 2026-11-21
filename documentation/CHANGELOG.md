# TransitIQ - Architecture & Implementation Changelog

This document tracks all architectural, database schema, and functional decisions and modifications throughout the development of TransitIQ, in compliance with **Section 21.8 (Change Management and Transparency)**.

Each entry records:
- **Date**: Date of change
- **Component Affected**: Database, Backend, Analytics, Dashboard, or Documentation
- **Previous Implementation / Baseline**: The original or prior design
- **New Implementation**: The modified or newly introduced design
- **Reason for Change**: Rationale based on data integrity, reliability, performance, or DP-900 alignment
- **Testing Performed**: Verification procedures executed

---

## Change Log Entries

### [2026-11-20] - Engineering Autonomy & Project Baseline Initialized
- **Component Affected**: Core Project Architecture & Governance
- **Previous Implementation / Baseline**: N/A (Fresh repository initialization)
- **New Implementation**: Established the project workspace, change management protocol, and DP-900 alignment framework under Section 21 Engineering Autonomy Guidelines.
- **Reason for Change**: Initial baseline setup for TransitIQ.
- **Testing Performed**: Workspace directory structure verified.

### [2026-11-20] - 3NF Relational Schema & Route Segments Junction Table
- **Component Affected**: Relational Database Schema (`sql/ddl/01_create_tables.sql`)
- **Previous Implementation / Baseline**: Unnormalized transit model where station sequences and route details risked transitive and partial functional dependencies.
- **New Implementation**: Formal Third Normal Form (3NF) relational design across six entities: `stops`, `routes`, `route_segments`, `vehicles`, `trips`, and `passenger_fares`. Added `route_segments` as a dedicated junction table with composite unique constraints `(route_id, stop_sequence)` and `(route_id, stop_id)`.
- **Reason for Change**: Eliminates insertion, update, and deletion anomalies when routes or stations are modified. Demonstrates DP-900 normalization standards.
- **Testing Performed**: Automated tests in `tests/test_database.py` verifying table creation, foreign key constraints, check constraints, and 3NF junction uniqueness.

### [2026-11-20] - Dual-Mode Database Connection Layer
- **Component Affected**: Database Connection Manager (`config/database_config.py`, `src/db/connection.py`)
- **Previous Implementation / Baseline**: Hardcoded local SQLite connection without cloud deployment path.
- **New Implementation**: Dual-mode connection manager using SQLAlchemy and raw sqlite3. Automatically reads `TRANSITIQ_DB_DIALECT`. If set to `azuresql` or `mssql`, dynamically connects to Azure SQL Database using ODBC Driver 18 with encryption; defaults to local SQLite file (`database/transitiq.db`) for offline zero-cost student demonstration.
- **Reason for Change**: Aligns with Section 21.2 (Technology Flexibility) and Section 21.4 (Autonomous Problem Solving), ensuring student viva demonstrations work offline without cloud bills while preserving 100% Azure SQL readiness.
- **Testing Performed**: Verified SQLite connection pooling and script execution in `tests/test_database.py`.

### [2026-11-20] - Windows File Lock Safe Database Initialization
- **Component Affected**: Database Connection Engine (`src/db/connection.py`)
- **Previous Implementation / Baseline**: `initialize_database(reset=True)` called `pathlib.Path.unlink()` to delete the database file on disk.
- **New Implementation**: Replaced disk file deletion with transactional `DROP VIEW IF EXISTS` and `DROP TABLE IF EXISTS` in reverse foreign key dependency order, disabling `foreign_keys` temporarily during reset. Disposes existing SQLAlchemy engine connection pools before dropping.
- **Reason for Change**: On Windows, open SQLite connection handles caused `PermissionError: [WinError 32] The process cannot access the file because it is being used by another process`.
- **Testing Performed**: Re-ran full test suite under pytest across multiple database resets without encountering file lock exceptions.

### [2026-11-20] - Multi-Modal Synthetic Data Generator with Active Dispatch States
- **Component Affected**: Data Seeding Module (`src/data/seed_data.py`)
- **Previous Implementation / Baseline**: Basic synthetic trips only generated historical completed or delayed states.
- **New Implementation**: Enhanced data generation across 12 station hubs, 6 multi-modal routes (Metro, BRT, Express, Commuter), 26 corridor segments, and 16 fleet assets. Trips now encompass active operational states (`Scheduled`, `In-Transit`, `Completed`, `Delayed`, `Cancelled`), and 2,200+ passenger ticketing transactions across 4 payment methods.
- **Reason for Change**: Ensures realistic demonstration of real-time seat booking (OLTP) and operational dispatch state transitions during academic viva.
- **Testing Performed**: Generated full dataset in under 5 seconds; verified via `src/data/csv_ingestion.py` audit score.

### [2026-11-20] - Analytical OLAP Layer & Interactive SQL Studio
- **Component Affected**: Analytical Views (`sql/ddl/02_create_views.sql`, `src/analytics/metrics_engine.py`)
- **Previous Implementation / Baseline**: Direct raw table queries without pre-aggregated analytical views.
- **New Implementation**: Created five high-performance analytical views: `v_route_performance`, `v_hourly_ridership`, `v_stop_demand_analytics`, `v_fleet_utilization`, and `v_delay_monitoring`. Implemented advanced SQL queries featuring Common Table Expressions (CTEs) and analytical window functions (`SUM() OVER()`).
- **Reason for Change**: Fulfills DP-900 Domain 4 requirements (Analytics Workloads on Azure / Azure Synapse concepts).
- **Testing Performed**: Validated aggregations, windowing outputs, and execution latencies in `tests/test_analytics.py`.

### [2026-11-20] - Automated Data Quality Auditor & Cloud CSV Staging Pipeline
- **Component Affected**: Data Governance & ETL Pipeline (`src/data/csv_ingestion.py`)
- **Previous Implementation / Baseline**: No data validation or export pipeline.
- **New Implementation**: Automated data hygiene auditor running 6 critical integrity checks (Stop code uniqueness, Trip referential integrity, Fare referential integrity, Non-negative fares, Fleet capacity constraints, and Geographic coordinate validity). Exports all tables to standard CSV format in `/data` for cloud data lake staging.
- **Reason for Change**: Demonstrates Azure Data Factory (ADF) ETL ingestion and Azure Blob Storage data lake staging.
- **Testing Performed**: Executed automated audit achieving 100.0% data health score (6/6 checks passed).

### [2026-11-20] - TransitIQ Professional Enterprise UI & Zero-Emoji Redesign
- **Component Affected**: User Interface Dashboard (`app/dashboard.py`)
- **Previous Implementation / Baseline**: Emojis scattered across headers, sidebar, cards, and buttons. Mapbox tile server rendered a blank square when running offline. Dark mode text contrast was low.
- **New Implementation**: High-end enterprise design overhaul:
  - Removed 100% of emojis/emotes across navigation, metrics, titles, and buttons.
  - Replaced the blank external raster tile map with an offline-resilient **Topological Transit Vector Map** rendered directly in Plotly Dark (`go.Scatter` vector lines connecting stations by route color, with node sizes reflecting passenger footfall).
  - Dark-mode enterprise palette (`#0f172a` slate background, `#1e293b` cards, `#f8fafc` high-contrast typography, and `#38bdf8` electric blue accents).
  - Streamlined navigation labels: `Overview`, `Corridors & Network`, `Ridership & Demand`, `Ticketing Operations`, `Fleet & Dispatch`, `Technical Architecture`.
- **Reason for Change**: User requested emoji removal, dark-mode visual polish, and resolution of the blank map box shown in testing.
- **Testing Performed**: Verified compilation, test suite execution (12/12 passing), and offline rendering of all Plotly figures.
