# INDUSTRIAL INTERNSHIP REPORT
## TRANSITIQ: INTELLIGENT PUBLIC TRANSIT ANALYTICS & DATA PLATFORM ALIGNED WITH MICROSOFT AZURE DATA FUNDAMENTALS (DP-900)

**Submitted in Partial Fulfillment of the Requirements for the Degree of**  
**Bachelor of Engineering in Computer Science and Engineering**  
*(Specialization: Cloud & Systems Engineering)*

**by**  
**Aryan**  
*(UID: ____________________)*

**Department of Computer Science and Engineering**  
**University Institute of Engineering (AIT - CSE)**  
**Chandigarh University, Gharuan**  
**November 2026**

---

## BONAFIDE CERTIFICATE

This is to certify that the industrial internship report entitled **"TRANSITIQ: INTELLIGENT PUBLIC TRANSIT ANALYTICS & DATA PLATFORM ALIGNED WITH MICROSOFT AZURE DATA FUNDAMENTALS (DP-900)"** submitted by **Aryan (UID: ____________________)** in partial fulfillment of the requirements for the award of the Degree of **Bachelor of Engineering in Computer Science and Engineering** is a bonafide record of the work carried out under my guidance and supervision at Chandigarh University, Gharuan.

**Signature of Program Leader:** ____________________  
**Name:** ____________________  
**Program Leader - Computer Science & Engineering**  
**Department of Computer Science and Engineering**  
**Chandigarh University, Gharuan**

*This project report was evaluated by us on: ____________________*

**INTERNAL EXAMINER:** ____________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **EXTERNAL EXAMINER:** ____________________

---

## DECLARATION BY CANDIDATE

I hereby declare that this industrial internship report entitled **"TRANSITIQ: INTELLIGENT PUBLIC TRANSIT ANALYTICS & DATA PLATFORM ALIGNED WITH MICROSOFT AZURE DATA FUNDAMENTALS (DP-900)"** has been prepared by me independently. No part of the report is plagiarized from other sources. All information, concepts, data schemas, and design principles included from external sources and literature have been duly cited and acknowledged. I aver that if any part of the report is found to be plagiarized, I shall take full academic responsibility for it.

**Signature of Candidate:** ____________________  
**Name:** Aryan  
**UID:** ____________________  
**Place:** Chandigarh University, Gharuan  
**Date:** ____________________

---

## ABSTRACT

Rapid urbanization and the proliferation of multimodal transit networks (metro rail, rapid bus transit, express shuttles, and commuter rail) have generated vast volumes of operational, sensor, and ticketing data. Public transit authorities face the persistent challenge of unifying high-velocity transactional operations (fare ticketing, card taps, vehicle dispatching) with deep, computationally intensive analytical processing (passenger demand forecasting, route efficiency analysis, schedule punctuality tracking). This industrial internship project presents **TransitIQ**, an enterprise-grade public transit data platform developed strictly in compliance with the competencies of the **Microsoft DP-900 (Azure Data Fundamentals)** curriculum.

The project formulates a robust relational database schema strictly normalized to **Third Normal Form (3NF)**. The schema isolates stations, routes, and fleet assets while decoupling the complex many-to-many relationship between transit corridors and physical station stops using an optimized junction table (`route_segments`). TransitIQ implements a dual-workload architecture that balances **Online Transaction Processing (OLTP)** and **Online Analytical Processing (OLAP)**. The OLTP subsystem guarantees ACID-compliant passenger ticketing with capacity checks, dynamic concession discounting, and atomic operational dispatch status transitions. The OLAP subsystem employs pre-computed analytical views, Common Table Expressions (CTEs), and analytical window functions to evaluate commercial route viability and hourly rush-hour crowding curves.

Furthermore, an automated data governance pipeline audits database hygiene across six integrity dimensions, achieving a **100% data quality score**, and stages structured tables as CSV datasets simulating Azure Data Factory ingestion into an Azure Blob Storage data lake. The system provides seamless dual-mode connectivity: running locally on an offline, zero-cost SQLite engine for student demonstration while supporting cloud-native Azure SQL Database deployment via environment variable configuration. An interactive, dark-theme Command Centre dashboard built with Streamlit and Plotly delivers intuitive operational monitoring, station topological mapping, digital boarding pass generation, and an embedded SQL execution lab.

**Keywords:** Public Transit Analytics, Microsoft DP-900, Azure Data Fundamentals, Third Normal Form (3NF), OLTP vs OLAP, Relational Database Modeling, Streamlit Command Centre, Data Governance, ACID Transactions, Azure SQL Database.

---

## TABLE OF CONTENTS

| Chapter No. | Title | Page No. |
| :--- | :--- | :--- |
| | **BONAFIDE CERTIFICATE** | ii |
| | **DECLARATION BY CANDIDATE** | iii |
| | **ABSTRACT** | iv |
| | **LIST OF SYMBOLS, ABBREVIATIONS & NOMENCLATURE** | vii |
| **1.** | **INTRODUCTION** | **1** |
| 1.1 | Statement of the Problem | 1 |
| 1.2 | Importance & Relevance of Modern Urban Transit Analytics | 2 |
| 1.3 | Related Literature & State-of-the-Art Review | 3 |
| 1.4 | Scope & Objectives of the Industrial Training | 4 |
| 1.5 | Organization of the Report | 5 |
| **2.** | **MICROSOFT AZURE DATA FUNDAMENTALS (DP-900) FRAMEWORK** | **6** |
| 2.1 | Core Data Concepts (Structured, Semi-Structured, Unstructured) | 6 |
| 2.2 | Transactional vs. Analytical Workloads (OLTP vs. OLAP) | 7 |
| 2.3 | Cloud Relational Database Services (Azure SQL Database) | 8 |
| 2.4 | Non-Relational & Object Storage (Azure Blob Storage / ADLS Gen2) | 9 |
| 2.5 | Modern Cloud Data Warehousing & ETL (Azure Synapse & ADF) | 10 |
| **3.** | **RELATIONAL DATABASE MODELING & 3NF NORMALIZATION ANALYSIS** | **11** |
| 3.1 | Entity Identification & Data Dictionary | 11 |
| 3.2 | 3NF Database Schema Architecture | 12 |
| 3.3 | Mathematical Normalization Proofs (1NF, 2NF, 3NF) | 13 |
| 3.4 | Referential Integrity, Keys & Constraint Enforcement | 15 |
| 3.5 | Performance Indexing Strategy | 16 |
| **4.** | **IMPLEMENTATION METHODOLOGY & SYSTEM ARCHITECTURE** | **17** |
| 4.1 | Dual-Mode Database Connection Layer (SQLite & Azure SQL) | 17 |
| 4.2 | OLTP Transaction Processing Engine (ACID Ticketing & Dispatch) | 18 |
| 4.3 | OLAP Analytical Engine & Pre-Computed Materialized Views | 19 |
| 4.4 | Data Governance, Automated Hygiene Auditor & CSV Staging Pipeline | 21 |
| 4.5 | User Interface Architecture (Modern Enterprise Command Centre) | 22 |
| **5.** | **WEEKLY INTERNSHIP TRAINING REPORT** | **24** |
| 5.1 | Week 1: Requirements Analysis, Problem Formulation & DP-900 Study | 24 |
| 5.2 | Week 2: Relational Schema Modeling, 3NF Normalization & DDL Design | 25 |
| 5.3 | Week 3: OLTP Transaction Engine & Multimodal Synthetic Data Seeding | 26 |
| 5.4 | Week 4: OLAP Views, CTEs, Windowing Queries & Analytics Engine | 27 |
| 5.5 | Week 5: Dashboard UI/UX Engineering, Data Governance & CSV Pipeline | 28 |
| 5.6 | Week 6: Verification, Automated Testing & Viva Voce Preparation | 29 |
| **6.** | **RESULTS, TESTING & PERFORMANCE EVALUATION** | **30** |
| 6.1 | Automated Unit & Integration Testing (12/12 Passing Suite) | 30 |
| 6.2 | Query Execution Latency & Performance Benchmarks | 31 |
| 6.3 | Data Quality Audit & Hygiene Scorecard (100% Score) | 32 |
| 6.4 | Operational Dashboard Verification & User Experience | 33 |
| **7.** | **CONCLUSIONS & RECOMMENDATIONS FOR FUTURE WORK** | **34** |
| 7.1 | Conclusions | 34 |
| 7.2 | Recommendations & Future Scope | 35 |
| | **APPENDICES** | **36** |
| | **REFERENCES** | **40** |

---

## LIST OF ABBREVIATIONS & NOMENCLATURE

- **1NF / 2NF / 3NF:** First / Second / Third Normal Form
- **ACID:** Atomicity, Consistency, Isolation, Durability
- **ADF:** Azure Data Factory (Cloud ETL/ELT Integration)
- **ADLS Gen2:** Azure Data Lake Storage Generation 2
- **AFC:** Automated Fare Collection (Turnstiles & Smartcards)
- **BRT:** Bus Rapid Transit
- **CTE:** Common Table Expression (`WITH` clause)
- **DDL:** Data Definition Language
- **DML:** Data Manipulation Language
- **DP-900:** Microsoft Certified: Azure Data Fundamentals
- **EMV:** Contactless Card Standard (Europay, Mastercard, Visa)
- **ETL:** Extract, Transform, Load
- **OLAP:** Online Analytical Processing
- **OLTP:** Online Transaction Processing
- **PK / FK:** Primary Key / Foreign Key
- **TDE:** Transparent Data Encryption
- **UPI:** Unified Payments Interface

---

## CHAPTER 1: INTRODUCTION

### 1.1 Statement of the Problem
Modern metropolitan areas rely heavily on multimodal public transportation systems comprising underground metro rails, suburban commuter trains, bus rapid transit (BRT) trunk lines, and feeder shuttles. Every vehicle movement and passenger trip generates millions of records: smartcard taps at turnstiles, ticket purchase events at automated counters, GPS location telemetry broadcast by on-board units, and timetable adherence records.

Transit management systems face an architectural dilemma:
- **OLTP Needs:** High-frequency atomic writes (turnstile taps and ticketing) requiring instant response times without locking.
- **OLAP Needs:** Computationally heavy queries spanning millions of rows across routes, hours, and demographic concession categories to plan network capacity.
- **Data Integrity Hazards:** Naive unnormalized tables duplicate station names and route distances, leading to catastrophic update and deletion anomalies.

TransitIQ resolves this tension through a 3NF relational architecture, an ACID transactional ticketing engine, and decoupled analytical materialized views.

---

## CHAPTER 5: WEEKLY INTERNSHIP TRAINING REPORT (DAY-BY-DAY LOGS)

### Week 1: Requirements Analysis, Problem Formulation & DP-900 Study
- **Day 1:** Conducted literature review on urban transit data challenges, automated fare collection (AFC), and multimodal network topologies.
- **Day 2:** Studied Microsoft Certified: Azure Data Fundamentals (DP-900) curriculum, focusing on relational vs. non-relational concepts and cloud database services.
- **Day 3:** Analyzed the dual-workload conflict: why running OLAP analytical queries on live OLTP ticketing databases causes lock contention and timeouts.
- **Day 4:** Defined the scope for TransitIQ: 6 multimodal corridors, 12 station hubs, rolling stock fleet management, and automated data governance.
- **Day 5:** Formulated the technical baseline, initialized project repository structure, and configured the Python virtual environment.

### Week 2: Relational Schema Modeling, 3NF Normalization & DDL Design
- **Day 1:** Identified core transit entities: `stops`, `routes`, `vehicles`, `trips`, and `passenger_fares`, establishing operational attributes.
- **Day 2:** Designed Third Normal Form (3NF) relational model, isolating physical stations from route definitions to eliminate update anomalies.
- **Day 3:** Engineered the `route_segments` junction entity to resolve the many-to-many relationship between corridors and stations.
- **Day 4:** Authored `01_create_tables.sql` DDL script, defining primary keys, foreign keys (`ON DELETE RESTRICT`), and check constraints.
- **Day 5:** Formulated performance indexing strategy and verified database creation using SQLite and SQLAlchemy connection engines.

### Week 3: OLTP Transaction Engine & Multimodal Synthetic Data Seeding
- **Day 1:** Developed `seed_data.py` to generate realistic transit data: 12 stations across Delhi NCR coordinates and 6 multimodal routes.
- **Day 2:** Populated 16 fleet assets spanning Electric buses, CNG buses, Metro rakes, and Double Deckers, establishing capacity limits.
- **Day 3:** Engineered synthetic operational trips across morning rush, midday, and evening rush hours, simulating delays and on-time performance.
- **Day 4:** Generated 2,200+ passenger ticketing transactions across 4 payment methods (Smartcard, UPI/QR, EMV, Cash) with concession pricing.
- **Day 5:** Built `transit_service.py` implementing ACID-compliant ticket booking routines and operational dispatch state machine updates.

### Week 4: OLAP Views, CTEs, Windowing Queries & Analytics Engine
- **Day 1:** Authored `02_create_views.sql` implementing `v_route_performance` and `v_hourly_ridership` views for high-performance aggregations.
- **Day 2:** Engineered `v_stop_demand_analytics`, `v_fleet_utilization`, and `v_delay_monitoring` views for operational metrics.
- **Day 3:** Developed advanced analytical SQL queries utilizing Common Table Expressions (CTEs) to evaluate route profitability and revenue per km.
- **Day 4:** Implemented analytical window functions (`SUM() OVER()` partitioned by date) to track intra-day cumulative revenue progression.
- **Day 5:** Constructed `metrics_engine.py` connecting the analytical SQL views to Python data structures and Pandas DataFrames.

### Week 5: Dashboard UI/UX Engineering, Data Governance & CSV Pipeline
- **Day 1:** Built the core Streamlit web application layout (`app/dashboard.py`) with executive KPI cards and operational insights.
- **Day 2:** Engineered the topological transit vector map in Plotly Dark, tracing route lines and rendering station footfall without external tile dependencies.
- **Day 3:** Designed the interactive visual station stepper timeline and developed the digital boarding pass rendering interface.
- **Day 4:** Built `csv_ingestion.py` implementing automated six-point data hygiene audits and CSV data lake staging exports.
- **Day 5:** Overhauled user interface styling to a clean, professional dark enterprise operations theme, eliminating all informal emojis.

### Week 6: Verification, Automated Testing & Viva Voce Preparation
- **Day 1:** Authored comprehensive automated test suite in pytest: `test_database.py` verifying constraints and 3NF junction uniqueness.
- **Day 2:** Developed `test_transactions.py` validating ACID ticket booking rollbacks and trip dispatch status transitions.
- **Day 3:** Created `test_analytics.py` validating OLAP view aggregations, mathematical consistency, and 100% data quality audit scores.
- **Day 4:** Resolved Windows file-lock exceptions (`WinError 32`) in database initialization logic, ensuring 12/12 tests pass cleanly.
- **Day 5:** Authored full institutional internship report, ERD documentation, Azure deployment guide, and viva voce presentation script.

---

## REFERENCES

1. Codd, E. F., "A Relational Model of Data for Large Shared Data Banks," *Communications of the ACM*, Vol. 13, No. 6, 1970, pp. 377-387.
2. Trépanier, M., Tranchant, N., and Chapleau, R., "Individual Trip Detection on a Large Public Transit Network with Smartcard Data," *Transportation Research Part C: Emerging Technologies*, Vol. 15, No. 4, 2007, pp. 248-261.
3. Pelletier, M. P., Trépanier, M., and Morency, C., "Smart Card Data in Public Transit Planning: A Review," *Transportation Research Part C: Emerging Technologies*, Vol. 19, No. 4, 2011, pp. 557-568.
4. Microsoft Corporation, "Microsoft Certified: Azure Data Fundamentals (Exam DP-900) Study Guide & Learning Paths," *Microsoft Learn Documentation*, 2026.
5. Date, C. J., *An Introduction to Database Systems*, 8th Edition, Addison-Wesley, Boston, 2004, pp. 345-388.
6. Silberschatz, A., Korth, H. F., and Sudarshan, S., *Database System Concepts*, 7th Edition, McGraw-Hill, New York, 2020.
7. Kleppmann, M., *Designing Data-Intensive Applications*, O'Reilly Media, Sebastopol, 2017.
8. McKinney, W., *Python for Data Analysis*, 3rd Edition, O'Reilly Media, 2022.
