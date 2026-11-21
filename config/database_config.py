"""
TransitIQ Database Configuration Module
Provides seamless dual-mode database support:
- Local SQLite Engine (zero cost, 100% offline, fully reproducible for college viva)
- Azure SQL Database / Microsoft SQL Server (cloud-ready, production DP-900 deployment)
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = BASE_DIR / "database"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
DATABASE_DIR.mkdir(exist_ok=True)

# Default Local SQLite Database Path
SQLITE_DB_PATH = DATABASE_DIR / "transitiq.db"

# Environment Variables for Azure SQL / SQL Server
DB_DIALECT = os.getenv("TRANSITIQ_DB_DIALECT", "sqlite").lower()  # 'sqlite' or 'mssql' / 'azuresql'
AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER", "transitiq-server.database.windows.net")
AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE", "transitiq_db")
AZURE_SQL_USERNAME = os.getenv("AZURE_SQL_USERNAME", "azureuser")
AZURE_SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD", "")
AZURE_SQL_DRIVER = os.getenv("AZURE_SQL_DRIVER", "ODBC Driver 18 for SQL Server")

def get_connection_string() -> str:
    """
    Constructs the SQLAlchemy connection URL according to the configured dialect.
    """
    if DB_DIALECT in ("mssql", "azuresql"):
        return (
            f"mssql+pyodbc://{AZURE_SQL_USERNAME}:{AZURE_SQL_PASSWORD}@"
            f"{AZURE_SQL_SERVER}:1433/{AZURE_SQL_DATABASE}"
            f"?driver={AZURE_SQL_DRIVER.replace(' ', '+')}&Encrypt=yes&TrustServerCertificate=no"
        )
    # Default to robust SQLite local database
    return f"sqlite:///{SQLITE_DB_PATH.as_posix()}"

def get_sqlite_path() -> Path:
    """Returns local SQLite file path."""
    return SQLITE_DB_PATH
