import pandas as pd
from pathlib import Path

# ============================================================
# 1. Project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# ============================================================
# 2. Load data
# ============================================================

orders = pd.read_csv(
    DATA_DIR / "orders.csv"
)

delivery_events = pd.read_csv(
    DATA_DIR / "delivery_events_incident.csv"
)

print("Data loaded successfully.")
print()

print(f"Orders: {len(orders):,}")
print(f"Delivery events: {len(delivery_events):,}")

# ============================================================
# 3. Filter Delivered orders
# ============================================================

delivered_orders = orders[
    orders["order_status"] == "Delivered"
].copy()

print()
print(f"Delivered orders: {len(delivered_orders):,}")

# ============================================================
# 4. Count Delivered events
# ============================================================

delivered_events = delivery_events[
    delivery_events["event_type"] == "Delivered"
]

event_counts = (
    delivered_events
    .groupby("order_id")
    .size()
    .reset_index(name="delivered_event_count")
)

# ============================================================
# 5. Join orders with event counts
# ============================================================

investigation = delivered_orders.merge(
    event_counts,
    on="order_id",
    how="left"
)

investigation["delivered_event_count"] = (
    investigation["delivered_event_count"]
    .fillna(0)
    .astype(int)
)

# ============================================================
# 6. Classify data quality
# ============================================================

def classify_quality(count):
    if count == 0:
        return "Missing Delivered Event"
    elif count == 1:
        return "Normal"
    else:
        return "Duplicate Delivered Event"


investigation["data_quality_status"] = (
    investigation["delivered_event_count"]
    .apply(classify_quality)
)

# ============================================================
# 7. Display summary
# ============================================================

print()
print("Data quality summary:")
print(
    investigation["data_quality_status"]
    .value_counts()
)

print()
print("Investigation sample:")
print(
    investigation[
        [
            "order_id",
            "hub_id",
            "order_status",
            "delivered_event_count",
            "data_quality_status"
        ]
    ]
    .head(10)
    .to_string(index=False)
)

# ============================================================
# 8. Save investigation results
# ============================================================

output_file = DATA_DIR / "incident_summary.csv"

investigation.to_csv(
    output_file,
    index=False
)

print()
print(f"Incident summary saved to:")
print(output_file)

# ============================================================
# 9. Analyze incidents by hub
# ============================================================

hub_summary = (
    investigation
    .groupby("hub_id")
    .agg(
        total_delivered_orders=("order_id", "count"),
        total_incidents=(
            "data_quality_status",
            lambda x: (x != "Normal").sum()
        )
    )
    .reset_index()
)

hub_summary["incident_rate_pct"] = (
    hub_summary["total_incidents"]
    / hub_summary["total_delivered_orders"]
    * 100
).round(2)

hub_summary = hub_summary.sort_values(
    "incident_rate_pct",
    ascending=False
)

print()
print("Incident summary by hub:")
print(
    hub_summary.to_string(index=False)
)

# ============================================================
# 10. Analyze IL01 incidents by date
# ============================================================

il01_incidents = investigation[
    (investigation["hub_id"] == "IL01") &
    (investigation["data_quality_status"] != "Normal")
].copy()

il01_incidents["created_at"] = pd.to_datetime(
    il01_incidents["created_at"]
)

il01_incidents["order_date"] = (
    il01_incidents["created_at"]
    .dt.date
)

daily_incidents = (
    il01_incidents
    .groupby("order_date")
    .agg(
        total_incidents=("order_id", "count"),
        missing_events=(
            "data_quality_status",
            lambda x: (x == "Missing Delivered Event").sum()
        ),
        duplicate_events=(
            "data_quality_status",
            lambda x: (x == "Duplicate Delivered Event").sum()
        )
    )
    .reset_index()
)

print()
print("IL01 incidents by date:")
print(
    daily_incidents.to_string(index=False)
)

# ============================================================
# 11. Detect invalid event timestamps
# ============================================================

delivery_events["event_time"] = pd.to_datetime(
    delivery_events["event_time"],
    format="mixed"
)

orders["created_at"] = pd.to_datetime(
    orders["created_at"],
    format="mixed"
)

timestamp_check = delivery_events.merge(
    orders[
        [
            "order_id",
            "created_at"
        ]
    ],
    on="order_id",
    how="inner"
)

invalid_timestamps = timestamp_check[
    timestamp_check["event_time"] < timestamp_check["created_at"]
].copy()

print()
print("Invalid event timestamps:")
print(f"Total invalid timestamps: {len(invalid_timestamps):,}")

print()
print("Invalid timestamps by hub:")

timestamp_by_hub = (
    invalid_timestamps
    .groupby("hub_id")
    .size()
    .reset_index(name="invalid_timestamp_count")
    .sort_values(
        "invalid_timestamp_count",
        ascending=False
    )
)

print(
    timestamp_by_hub.to_string(index=False)
)

# ============================================================
# 12. Investigate missing Delivered events
# ============================================================

missing_orders = investigation[
    investigation["data_quality_status"] == "Missing Delivered Event"
][
    [
        "order_id",
        "hub_id"
    ]
].copy()

# Add order information
missing_orders = missing_orders.merge(
    orders[
        [
            "order_id",
            "created_at",
            "estimated_delivery_date"
        ]
    ],
    on="order_id",
    how="left"
)

# Count all events recorded for missing orders
missing_event_check = delivery_events.merge(
    missing_orders[["order_id"]],
    on="order_id",
    how="inner"
)

event_pattern = (
    missing_event_check
    .groupby(["order_id", "event_type"])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)

missing_orders = missing_orders.merge(
    event_pattern,
    on="order_id",
    how="left"
)

# Make sure expected event columns exist
for event_type in [
    "Picked Up",
    "Arrived at Hub",
    "Out for Delivery",
    "Delivered"
]:
    if event_type not in missing_orders.columns:
        missing_orders[event_type] = 0

print()
print("Missing Delivered Event investigation:")

print(
    missing_orders[
        [
            "order_id",
            "hub_id",
            "Picked Up",
            "Arrived at Hub",
            "Out for Delivery",
            "Delivered",
            "estimated_delivery_date"
        ]
    ]
    .head(10)
    .to_string(index=False)
)

# ============================================================
# 13. Investigate duplicate Delivered events
# ============================================================

duplicate_orders = investigation[
    investigation["data_quality_status"] == "Duplicate Delivered Event"
][
    [
        "order_id",
        "hub_id",
        "delivered_event_count"
    ]
].copy()

duplicate_event_details = delivery_events[
    delivery_events["event_type"] == "Delivered"
].merge(
    duplicate_orders[["order_id"]],
    on="order_id",
    how="inner"
)

duplicate_event_details["event_time"] = pd.to_datetime(
    duplicate_event_details["event_time"],
    format="mixed"
)

duplicate_event_details = duplicate_event_details.sort_values(
    ["order_id", "event_time"]
)

# Calculate time gap between duplicate events
duplicate_event_details["previous_event_time"] = (
    duplicate_event_details
    .groupby("order_id")["event_time"]
    .shift(1)
)

duplicate_event_details["duplicate_gap_minutes"] = (
    (
        duplicate_event_details["event_time"]
        - duplicate_event_details["previous_event_time"]
    )
    .dt.total_seconds()
    / 60
)

print()
print("Duplicate Delivered Event investigation:")

print(
    duplicate_event_details[
        [
            "order_id",
            "hub_id",
            "event_time",
            "previous_event_time",
            "duplicate_gap_minutes"
        ]
    ]
    .head(20)
    .to_string(index=False)
)

# ============================================================
# 14. Analyze duplicate event pattern
# ============================================================

duplicate_pattern = (
    duplicate_event_details
    .groupby("hub_id")
    .agg(
        affected_orders=("order_id", "nunique"),
        duplicate_events=("order_id", "count")
    )
    .reset_index()
)

duplicate_pattern["duplicate_events_per_order"] = (
    duplicate_pattern["duplicate_events"]
    / duplicate_pattern["affected_orders"]
).round(2)

print()
print("Duplicate event pattern by hub:")
print(
    duplicate_pattern
    .sort_values(
        "affected_orders",
        ascending=False
    )
    .to_string(index=False)
)

# Check whether duplicate timestamps are identical
duplicate_gap_summary = (
    duplicate_event_details[
        duplicate_event_details["duplicate_gap_minutes"].notna()
    ]
    .groupby("duplicate_gap_minutes")
    .size()
    .reset_index(name="order_count")
    .sort_values("duplicate_gap_minutes")
)

print()
print("Duplicate timestamp gap distribution:")
print(
    duplicate_gap_summary
    .to_string(index=False)
)

# ============================================================
# 15. Analyze IL01 incidents by hour
# ============================================================

il01_incident_events = duplicate_event_details[
    duplicate_event_details["hub_id"] == "IL01"
].copy()

il01_incident_events["event_hour"] = (
    il01_incident_events["event_time"]
    .dt.hour
)

hourly_duplicate_pattern = (
    il01_incident_events
    .groupby("event_hour")
    .size()
    .reset_index(name="duplicate_event_count")
    .sort_values("event_hour")
)

print()
print("IL01 duplicate events by hour:")
print(
    hourly_duplicate_pattern
    .to_string(index=False)
)

# ============================================================
# 16. Cross-check incident overlap
# ============================================================

missing_order_ids = set(
    investigation.loc[
        investigation["data_quality_status"] == "Missing Delivered Event",
        "order_id"
    ]
)

duplicate_order_ids = set(
    investigation.loc[
        investigation["data_quality_status"] == "Duplicate Delivered Event",
        "order_id"
    ]
)

invalid_timestamp_order_ids = set(
    invalid_timestamps["order_id"]
)

print()
print("Incident overlap analysis:")

print(
    f"Missing Delivered Event orders: "
    f"{len(missing_order_ids)}"
)

print(
    f"Duplicate Delivered Event orders: "
    f"{len(duplicate_order_ids)}"
)

print(
    f"Invalid timestamp orders: "
    f"{len(invalid_timestamp_order_ids)}"
)

print()
print("Overlap between incident types:")

print(
    f"Missing + Duplicate: "
    f"{len(missing_order_ids & duplicate_order_ids)}"
)

print(
    f"Missing + Invalid Timestamp: "
    f"{len(missing_order_ids & invalid_timestamp_order_ids)}"
)

print(
    f"Duplicate + Invalid Timestamp: "
    f"{len(duplicate_order_ids & invalid_timestamp_order_ids)}"
)

print(
    f"All three: "
    f"{len(missing_order_ids & duplicate_order_ids & invalid_timestamp_order_ids)}"
)
# ============================================================
# 17. Create incident summary for support review
# ============================================================

incident_summary = pd.DataFrame({
    "incident_type": [
        "Missing Delivered Event",
        "Duplicate Delivered Event",
        "Invalid Event Timestamp"
    ],
    "affected_orders": [
        len(missing_order_ids),
        len(duplicate_order_ids),
        len(invalid_timestamp_order_ids)
    ],
    "primary_hub": [
        "IL01",
        "IL01",
        "Multiple Hubs"
    ],
    "key_finding": [
        "Upstream delivery events exist, but final Delivered event is missing.",
        "Two identical Delivered events exist with a 0-minute timestamp gap.",
        "Event timestamp occurs before the order creation timestamp."
    ]
})

summary_file = DATA_DIR / "incident_type_summary.csv"

incident_summary.to_csv(
    summary_file,
    index=False
)

print()
print("Incident type summary:")
print(
    incident_summary.to_string(index=False)
)

print()
print(f"Incident type summary saved to:")
print(summary_file)