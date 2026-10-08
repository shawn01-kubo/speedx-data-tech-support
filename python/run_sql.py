import duckdb
import sys
from pathlib import Path

# ============================================================
# Project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = PROJECT_ROOT / "sql"

# ============================================================
# Check command-line argument
# ============================================================

if len(sys.argv) != 2:
    print("Usage:")
    print("  python python/run_sql.py 01")
    print("  python python/run_sql.py 02")
    print("  python python/run_sql.py 03")
    sys.exit(1)

query_number = sys.argv[1]

# ============================================================
# Map query number to SQL file
# ============================================================

sql_files = {
    "01": "01_delivery_event_reconciliation.sql",
    "02": "02_incident_rate.sql",
    "03": "03_timestamp_quality.sql",
}

if query_number not in sql_files:
    print(f"Unknown SQL query: {query_number}")
    print("Available queries: 01, 02, 03")
    sys.exit(1)

sql_file = SQL_DIR / sql_files[query_number]

# ============================================================
# Read SQL
# ============================================================

with open(sql_file, "r", encoding="utf-8") as f:
    sql = f.read()

# ============================================================
# Execute SQL
# ============================================================

print("=" * 70)
print(f"Running: {sql_file.name}")
print("=" * 70)
print()

result = duckdb.sql(sql)

print(result)