-- ============================================================
-- SpeedX Data & Tech Support Project
-- SQL Investigation #1
-- Delivery Event Reconciliation
-- ============================================================

WITH delivery_check AS (

    SELECT
        o.order_id,
        o.hub_id,
        o.order_status,
        COUNT(e.event_id) AS delivered_event_count

    FROM read_csv_auto('data/orders.csv') o

    LEFT JOIN read_csv_auto('data/delivery_events_incident.csv') e
        ON o.order_id = e.order_id
        AND e.event_type = 'Delivered'

    WHERE o.order_status = 'Delivered'

    GROUP BY
        o.order_id,
        o.hub_id,
        o.order_status
)

SELECT
    order_id,
    hub_id,
    order_status,
    delivered_event_count,

    CASE
        WHEN delivered_event_count = 0
            THEN 'Missing Delivered Event'

        WHEN delivered_event_count = 1
            THEN 'Normal'

        WHEN delivered_event_count > 1
            THEN 'Duplicate Delivered Event'
    END AS data_quality_status

FROM delivery_check

ORDER BY
    delivered_event_count,
    order_id;