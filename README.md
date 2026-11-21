# 🚆 TransitIQ: Public Transit Analytics & Intelligence System

**Microsoft DP-900 (Azure Data Fundamentals) Capstone Project**  
*An enterprise-grade, student-level public transit data platform featuring 3NF relational modeling, dual OLTP/OLAP workloads, automated data governance, and an interactive Streamlit Command Centre.*

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Database-SQLite/AzureSQL](https://img.shields.io/badge/Database-SQLite%20%7C%20Azure%20SQL-0078D4.svg)](https://azure.microsoft.com/services/sql-database/)
[![Framework-Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Standard-DP900](https://img.shields.io/badge/Certification-DP--900-brightgreen.svg)](https://learn.microsoft.com/credentials/certifications/azure-data-fundamentals/)

---

## 📌 Executive Summary

Modern urban transit authorities generate millions of transactional and sensor events daily—smartcard taps, bus GPS telemetry, fleet maintenance logs, and scheduling records. **TransitIQ** demonstrates how modern cloud data architectures bridge the gap between **high-velocity transactional processing (OLTP)** and **deep business intelligence (OLAP)**.

Developed specifically to demonstrate competencies evaluated in the **Microsoft DP-900 (Azure Data Fundamentals)** certification:
- **Relational Modeling:** Strict Third Normal Form (3NF) database schema with PK/FK constraints, cascading policies, and indexes.
- **Dual-Mode Storage:** Offline zero-cost local SQLite engine with drop-in configuration for cloud-native **Azure SQL Database**.
- **OLTP Transaction Engine:** ACID-compliant ticket issuing and real-time trip dispatch with capacity validation.
- **OLAP Analytical Layer:** Pre-computed analytical views, Common Table Expressions (CTEs), and SQL window functions (`SUM() OVER()`).
- **Data Governance:** Automated data quality auditor checking referential integrity, coordinate bounds, and anomaly scores.
- **Interactive Command Centre:** Multi-tab Streamlit & Plotly dashboard for live operations, ridership curves, and fleet readiness.

---

## 🏛️ System Architecture

```
DPAS/
│
├── app/
│   └── dashboard.py            # Streamlit Multi-Page Command Centre
│
├── config/
│   ├── __init__.py
│   └── database_config.py      # Dual-mode DB Engine (SQLite / Azure SQL)
│
├── src/
│   ├── analytics/
│   │   └── metrics_engine.py   # High-performance OLAP KPI computations
│   ├── data/
│   │   ├── seed_data.py        # Realistic multi-modal transit data generator
│   │   └── csv_ingestion.py    # CSV batch pipeline & Data Quality Auditor
│   ├── db/
│   │   └── connection.py       # Thread-safe connection & transaction runner
│   ├── models/
│   │   └── entities.py         # 3NF Dataclass entities & schemas
│   └── services/
│       └── transit_service.py  # OLTP business logic (ticketing, dispatch)
│
├── sql/
│   ├── ddl/
│   │   ├── 01_create_tables.sql       # 3NF relational tables & constraints
│   │   ├── 02_create_views.sql        # Analytical OLAP views
│   │   └── 03_create_procedures.sql   # Transactional stored procedures
│   └── queries/
│       ├── 01_oltp_operations.sql     # OLTP ticketing & updates
│       └── 02_olap_analytics.sql      # Multi-table CTEs & window functions
│
├── tests/
│   ├── test_database.py        # Schema integrity & 3NF constraint tests
│   ├── test_transactions.py    # ACID compliance & ticket booking tests
│   └── test_analytics.py       # Analytical calculations & KPI tests
│
├── documentation/
│   ├── CHANGELOG.md            # Change management log (Section 21.8)
│   ├── ERD_DIAGRAM.md          # Mermaid ER diagrams & Normalization proofs
│   ├── AZURE_DEPLOYMENT_GUIDE.md # Azure SQL, Blob & Synapse deployment
│   └── TRANSITIQ_DP900_REPORT.md # Academic Project Report (Viva-ready)
│
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10 or higher.
- Windows, macOS, or Linux.

### 2. Setup Virtual Environment & Dependencies
```powershell
# Clone or navigate to the project directory
cd c:\Users\ARYAN\Desktop\DPAS

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 3. Initialize Database & Seed Realistic Transit Data
```powershell
python src/data/seed_data.py
```
*Populates 12 stations, 6 multi-modal routes, 42 corridor segments, 16 vehicle assets, 160 scheduled trips, and 2,200+ passenger ticketing transactions.*

### 4. Launch TransitIQ Command Centre
```powershell
streamlit run app/dashboard.py
```
Open your browser at `http://localhost:8501`.

### 5. Run Automated Test Suite
```powershell
pytest -v
```

---

## 🎛️ Command Centre Modules

1. **📊 Executive Overview:** Real-time KPI summary (Active routes, fleet size, trips, on-time percentage, ridership, and revenue) with interactive Plotly visuals.
2. **🗺️ Route Network & Hubs:** Geospatial station analytics, busiest transfer hubs, and corridor sequence inspector.
3. **👥 Passenger Ridership & Revenue:** Hourly ridership demand curve (identifying peak rush hours 08:00-10:00 & 17:00-19:00), concession demographics, and payment channel breakdown.
4. **🚍 Fleet & Punctuality:** Fleet propulsion distribution (Electric, CNG, Hybrid), vehicle load factors, and delay severity classifications.
5. **⚡ OLTP Ticketing & Dispatch:** Interactive transactional booking with ACID rollback protection and real-time operational trip dispatch.
6. **🔍 SQL Studio & DP-900 Architecture:** Interactive query runner showcasing 3NF normalization proofs, CTEs, and SQL window functions with execution latency metrics.
7. **🛡️ Data Quality & Azure Ingestion:** Automated data hygiene checklist, 100% data health verification, and one-click CSV export simulating cloud data staging.

---

## 🎓 Academic Viva Voce Highlights

- **Why 3NF?** Separates `stops` from `routes` and `trips`, eliminating update anomalies when station coordinates or route attributes change.
- **Why dual-mode DB?** Enables 100% offline student demonstration with SQLite while supporting drop-in production deployment to **Azure SQL Database** via environment variables.
- **How is OLTP different from OLAP?** OLTP focuses on fast, atomic, single-row inserts/updates (`passenger_fares`), whereas OLAP runs multi-table aggregations over thousands of rows (`v_route_performance`).
