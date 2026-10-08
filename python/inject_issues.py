import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# 1. Project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


# ============================================================
# 2. Load existing datasets
# ============================================================

orders = pd.read_csv(
    DATA_DIR / "orders.csv"
)

delivery_events = pd.read_csv(
    DATA_DIR / "delivery_events.csv"
)


# ============================================================
# 3. Reproducibility
# ============================================================

np.random.seed(42)


# ============================================================
# 4. Create Issue #1
#    Delivered orders missing Delivered event
# ============================================================

delivered_orders = orders[
    orders["order_status"] == "Delivered"
].copy()

# Select 150 delivered orders from IL01
issue_1_orders = delivered_orders[
    delivered_orders["hub_id"] == "IL01"
].sample(
    n=150,
    random_state=42
)

issue_1_order_ids = set(
    issue_1_orders["order_id"]
)

delivery_events = delivery_events[
    ~(
        delivery_events["order_id"].isin(issue_1_order_ids)
        &
        (delivery_events["event_type"] == "Delivered")
    )
]


# ============================================================
# 5. Create Issue #2
#    Duplicate Delivered events
# ============================================================

duplicate_source = delivered_orders[
    delivered_orders["hub_id"] == "IL01"
].sample(
    n=75,
    random_state=123
)

duplicate_events = delivery_events[
    delivery_events["order_id"].isin(
        duplicate_source["order_id"]
    )
    &
    (delivery_events["event_type"] == "Delivered")
].copy()

duplicate_events["event_id"] = (
    "DUP"
    + duplicate_events["event_id"].str[3:]
)

delivery_events = pd.concat(
    [
        delivery_events,
        duplicate_events
    ],
    ignore_index=True
)


# ============================================================
# 6. Create Issue #3
#    Invalid / suspicious timestamps
# ============================================================

timestamp_source = delivered_orders.sample(
    n=50,
    random_state=456
)

timestamp_order_ids = set(
    timestamp_source["order_id"]
)

mask = (
    delivery_events["order_id"].isin(timestamp_order_ids)
    &
    (delivery_events["event_type"] == "Delivered")
)

delivery_events.loc[
    mask,
    "event_time"
] = "2026-09-01 10:00:00"


# ============================================================
# 7. Save incident dataset
# ============================================================

delivery_events.to_csv(
    DATA_DIR / "delivery_events_incident.csv",
    index=False
)


# ============================================================
# 8. Summary
# ============================================================

print("Incident data generation completed.")
print()

print(
    f"Issue #1 - Missing Delivered events: "
    f"{len(issue_1_orders)}"
)

print(
    f"Issue #2 - Duplicate Delivered events: "
    f"{len(duplicate_events)}"
)

print(
    f"Issue #3 - Suspicious timestamps: "
    f"{len(timestamp_source)}"
)

print()
print("Incident dataset saved to:")
print(
    DATA_DIR / "delivery_events_incident.csv"
)