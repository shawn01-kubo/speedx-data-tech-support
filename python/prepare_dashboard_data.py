import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

orders = pd.read_csv(DATA_DIR / "orders.csv")

investigation = pd.read_csv(
    DATA_DIR / "incident_summary.csv"
)

print("Dashboard data preparation started.")
print()

print(f"Orders loaded: {len(orders):,}")
print(
    f"Investigation records loaded: "
    f"{len(investigation):,}"
)

delivered_orders = orders[
    orders["order_status"] == "Delivered"
].copy()

print(
    f"Delivered orders: "
    f"{len(delivered_orders):,}"
)

hub_kpi = (
    investigation
    .groupby("hub_id")
    .agg(
        total_delivered_orders=("order_id", "count"),
        incident_orders=(
            "data_quality_status",
            lambda x: (x != "Normal").sum()
        )
    )
    .reset_index()
)

hub_kpi["incident_rate_pct"] = (
    hub_kpi["incident_orders"]
    / hub_kpi["total_delivered_orders"]
).round(4)

hub_kpi = hub_kpi.sort_values(
    "incident_rate_pct",
    ascending=False
)

print()
print("Hub KPI:")
print(
    hub_kpi.to_string(index=False)
)

hub_kpi_file = DATA_DIR / "dashboard_hub_kpi.csv"

hub_kpi.to_csv(
    hub_kpi_file,
    index=False
)

print()
print("Hub KPI saved to:")
print(hub_kpi_file)

incident_type_kpi = (
    investigation["data_quality_status"]
    .value_counts()
    .reset_index()
)

incident_type_kpi.columns = [
    "incident_type",
    "affected_orders"
]

invalid_timestamp_row = pd.DataFrame({
    "incident_type": ["Invalid Event Timestamp"],
    "affected_orders": [50]
})

incident_type_kpi = pd.concat(
    [
        incident_type_kpi[
            incident_type_kpi["incident_type"] != "Normal"
        ],
        invalid_timestamp_row
    ],
    ignore_index=True
)

print()
print("Incident Type KPI:")
print(
    incident_type_kpi.to_string(index=False)
)

incident_type_file = (
    DATA_DIR / "dashboard_incident_type_kpi.csv"
)

incident_type_kpi.to_csv(
    incident_type_file,
    index=False
)

print()
print("Incident Type KPI saved to:")
print(incident_type_file)

il01_incidents = investigation[
    (investigation["hub_id"] == "IL01") &
    (investigation["data_quality_status"] != "Normal")
].copy()

il01_incidents["created_at"] = pd.to_datetime(
    il01_incidents["created_at"],
    format="mixed"
)

il01_incidents["order_date"] = (
    il01_incidents["created_at"]
    .dt.date
)

daily_incident_kpi = (
    il01_incidents
    .groupby("order_date")
    .agg(
        total_incidents=("order_id", "count"),
        missing_events=(
            "data_quality_status",
            lambda x: (
                x == "Missing Delivered Event"
            ).sum()
        ),
        duplicate_events=(
            "data_quality_status",
            lambda x: (
                x == "Duplicate Delivered Event"
            ).sum()
        )
    )
    .reset_index()
)

print()
print("Daily Incident KPI:")
print(
    daily_incident_kpi.to_string(index=False)
)

daily_incident_file = (
    DATA_DIR / "dashboard_daily_incident_kpi.csv"
)

daily_incident_kpi.to_csv(
    daily_incident_file,
    index=False
)

print()
print("Daily Incident KPI saved to:")
print(daily_incident_file)