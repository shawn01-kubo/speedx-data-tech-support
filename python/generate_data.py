import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# 1. Project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

DATA_DIR.mkdir(exist_ok=True)


# ============================================================
# 2. Basic configuration
# ============================================================

np.random.seed(42)

NUM_ORDERS = 10000

HUBS = [
    "IL01",
    "NJ01",
    "TX01",
    "CA01",
]


# ============================================================
# 3. Generate hubs
# ============================================================

hubs = pd.DataFrame({
    "hub_id": HUBS,
    "hub_name": [
        "Chicago Hub",
        "New Jersey Hub",
        "Dallas Hub",
        "Los Angeles Hub",
    ],
    "state": [
        "IL",
        "NJ",
        "TX",
        "CA",
    ]
})


# ============================================================
# 4. Generate orders
# ============================================================

order_ids = [
    f"ORD{i:06d}"
    for i in range(1, NUM_ORDERS + 1)
]

tracking_numbers = [
    f"SX{i:08d}"
    for i in range(1, NUM_ORDERS + 1)
]

customer_ids = np.random.randint(
    10000,
    20000,
    NUM_ORDERS
)

hub_ids = np.random.choice(
    HUBS,
    NUM_ORDERS,
    p=[0.40, 0.25, 0.20, 0.15]
)

statuses = np.random.choice(
    [
        "Delivered",
        "In Transit",
        "Out for Delivery",
        "Exception"
    ],
    NUM_ORDERS,
    p=[0.70, 0.18, 0.08, 0.04]
)

created_dates = pd.date_range(
    start="2026-10-01",
    end="2026-10-07",
    periods=NUM_ORDERS
)

estimated_dates = (
    created_dates
    + pd.to_timedelta(
        np.random.randint(1, 4, NUM_ORDERS),
        unit="D"
    )
)

orders = pd.DataFrame({
    "order_id": order_ids,
    "tracking_number": tracking_numbers,
    "customer_id": customer_ids,
    "hub_id": hub_ids,
    "order_status": statuses,
    "created_at": created_dates,
    "estimated_delivery_date": estimated_dates.date,
})


# ============================================================
# 5. Generate delivery events
# ============================================================

event_types = [
    "Picked Up",
    "Arrived at Hub",
    "Out for Delivery",
    "Delivered"
]

events = []

event_id = 1

for _, order in orders.iterrows():

    order_id = order["order_id"]
    hub_id = order["hub_id"]
    order_status = order["order_status"]
    created_at = order["created_at"]

    # Every order gets the first three events
    base_events = [
        "Picked Up",
        "Arrived at Hub",
        "Out for Delivery"
    ]

    for i, event_type in enumerate(base_events):

        events.append({
            "event_id": f"EVT{event_id:07d}",
            "order_id": order_id,
            "hub_id": hub_id,
            "event_type": event_type,
            "event_time": (
                created_at
                + pd.Timedelta(hours=(i + 1) * 6)
            )
        })

        event_id += 1

    # Delivered orders normally get a Delivered event
    if order_status == "Delivered":

        events.append({
            "event_id": f"EVT{event_id:07d}",
            "order_id": order_id,
            "hub_id": hub_id,
            "event_type": "Delivered",
            "event_time": created_at + pd.Timedelta(hours=24)
        })

        event_id += 1


delivery_events = pd.DataFrame(events)


# ============================================================
# 6. Save datasets
# ============================================================

hubs.to_csv(
    DATA_DIR / "hubs.csv",
    index=False
)

orders.to_csv(
    DATA_DIR / "orders.csv",
    index=False
)

delivery_events.to_csv(
    DATA_DIR / "delivery_events.csv",
    index=False
)


# ============================================================
# 7. Print summary
# ============================================================

print("Data generation completed.")
print()

print(f"Orders: {len(orders):,}")
print(f"Delivery events: {len(delivery_events):,}")
print(f"Hubs: {len(hubs):,}")

print()
print("Order status distribution:")
print(orders["order_status"].value_counts())

print()
print("Files saved to:")
print(DATA_DIR)