# Incident Report: Delivery Data Quality Issues

## 1. Incident Summary

A data-quality investigation identified delivery-event issues in the synthetic last-mile delivery dataset.

The primary concentration of missing and duplicate delivery-event issues was observed at the IL01 hub.

Across 6,915 delivered orders:

- 150 orders had missing Delivered events.
- 73 orders had duplicate Delivered events.
- 50 orders had invalid event timestamps.

The missing and duplicate event issues were concentrated at IL01.

---

## 2. Impact

IL01 had:

- 2,768 delivered orders
- 223 data-quality incidents
- 8.06% incident rate

The other hubs had a 0% incident rate for missing or duplicate Delivered events.

These data-quality issues could affect:

- Delivery status reporting
- Operational dashboards
- KPI calculations
- Order-level delivery tracking
- Downstream analytics

---

## 3. Investigation Approach

The investigation used SQL and Python to:

1. Reconcile Delivered orders against delivery events.
2. Identify missing and duplicate Delivered events.
3. Compare incident rates across hubs.
4. Analyze incident patterns by date and hour.
5. Validate event timestamps against order creation timestamps.
6. Check whether different incident types overlapped.
7. Investigate event patterns for affected orders.

---

## 4. Key Findings

### 4.1 Missing Delivered Events

150 IL01 orders were classified as having a missing Delivered event.

The affected orders generally contained:

- Picked Up
- Arrived at Hub
- Out for Delivery

but did not contain the final Delivered event.

This suggests that the issue is concentrated around the final delivery-event recording or ingestion step rather than the entire order-event pipeline.

---

### 4.2 Duplicate Delivered Events

73 IL01 orders contained duplicate Delivered events.

Each affected order had two Delivered records with an identical timestamp.

The timestamp gap analysis showed:

- 73 affected orders
- 146 Delivered event records
- 0-minute timestamp gap for all duplicate pairs

This pattern is more consistent with duplicate event recording or ingestion behavior than two separate delivery actions.

Application or API logs would be required to determine the exact technical root cause.

---

### 4.3 Invalid Event Timestamps

50 events contained timestamps earlier than the associated order creation timestamp.

The invalid timestamps were distributed across multiple hubs:

- IL01: 27
- NJ01: 10
- CA01: 9
- TX01: 4

This indicates that the timestamp issue is broader than the IL01-specific missing and duplicate event issues.

---

### 4.4 Incident Pattern

IL01 incidents occurred across multiple dates from October 1 through October 6.

The daily incident counts ranged from 34 to 39.

The duplicate events did not show a clear concentration within a single hour of the day.

Therefore, the available data does not support attributing the issue to a specific time window.

---

### 4.5 Incident Overlap

The three incident categories did not overlap at the order level.

| Incident Type | Affected Orders |
|---|---:|
| Missing Delivered Event | 150 |
| Duplicate Delivered Event | 73 |
| Invalid Event Timestamp | 50 |

Overlap between all incident categories was 0.

This suggests that the issues represent separate data-quality patterns rather than multiple symptoms occurring on the same orders.

---

## 5. Preliminary Root Cause Assessment

Based on the available data:

### Missing Delivered Events

Likely related to the recording or ingestion of the final Delivered event.

### Duplicate Delivered Events

Likely related to duplicate event recording or ingestion.

The identical timestamps across duplicate records provide evidence for this hypothesis.

### Invalid Timestamps

Likely related to timestamp validation, event-time generation, or upstream data handling.

The current dataset does not contain sufficient system-level information to identify the exact source.

---

## 6. Recommended Next Steps

1. Review application and API logs for affected IL01 orders.
2. Check whether duplicate events originate upstream or during ingestion.
3. Review event-processing and retry behavior.
4. Add validation to prevent duplicate Delivered events.
5. Add timestamp validation against order creation time.
6. Monitor IL01 delivery-event quality through a recurring dashboard.
7. Add automated alerts for abnormal incident rates.

---

## 7. Validation Plan

After remediation, validate that:

- Missing Delivered event rate decreases.
- Duplicate Delivered event rate decreases.
- Invalid timestamp count reaches zero.
- IL01 incident rate returns to the expected baseline.
- No new duplicate Delivered records are introduced.
- Delivery dashboards reconcile with source event data.