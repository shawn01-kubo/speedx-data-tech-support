-- ============================================================
-- SpeedX Data & Tech Support Project
-- SQL Investigation #3
-- Event Timestamp Quality
-- ============================================================

SELECT
    e.event_id,
    e.order_id,
    o.hub_id,
    o.created_at AS order_created_at,
    e.event_time,
    e.event_type

FROM read_csv_auto('data/orders.csv') o

INNER JOIN read_csv_auto('data/delivery_events_incident.csv') e
    ON o.order_id = e.order_id

WHERE
    CAST(e.event_time AS TIMESTAMP)
    < CAST(o.created_at AS TIMESTAMP)

ORDER BY
    e.event_time;