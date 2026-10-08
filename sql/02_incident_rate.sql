-- ============================================================
-- SpeedX Data & Tech Support Project
-- SQL Investigation #6
-- Hub Incident Rate
-- ============================================================

WITH delivery_check AS (

    SELECT
        o.order_id,
        o.hub_id,
        COUNT(e.event_id) AS delivered_event_count

    FROM read_csv_auto('data/orders.csv') o

    LEFT JOIN read_csv_auto('data/delivery_events_incident.csv') e
        ON o.order_id = e.order_id
        AND e.event_type = 'Delivered'

    WHERE o.order_status = 'Delivered'

    GROUP BY
        o.order_id,
        o.hub_id
),

classified AS (

    SELECT
        order_id,
        hub_id,

        CASE
            WHEN delivered_event_count = 0
                THEN 'Missing'

            WHEN delivered_event_count = 1
                THEN 'Normal'

            ELSE 'Duplicate'
        END AS quality_status

    FROM delivery_check
)

SELECT
    hub_id,

    COUNT(*) AS total_delivered_orders,

    SUM(
        CASE
            WHEN quality_status = 'Missing'
                THEN 1
            ELSE 0
        END
    ) AS missing_events,

    SUM(
        CASE
            WHEN quality_status = 'Duplicate'
                THEN 1
            ELSE 0
        END
    ) AS duplicate_events,

    SUM(
        CASE
            WHEN quality_status != 'Normal'
                THEN 1
            ELSE 0
        END
    ) AS total_incidents,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN quality_status != 'Normal'
                    THEN 1
                ELSE 0
            END
        )
        / COUNT(*),
        2
    ) AS incident_rate_pct

FROM classified

GROUP BY
    hub_id

ORDER BY
    incident_rate_pct DESC;