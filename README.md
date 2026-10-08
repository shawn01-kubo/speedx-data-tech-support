# SpeedX Last-Mile Delivery Data & Tech Support Project

## Project Overview

This project simulates a last-mile delivery data and technical support workflow.

The goal is to investigate delivery data quality issues, identify incident patterns, determine affected hubs, and communicate findings through SQL, Python, Power BI, and an incident report.

The project follows a practical support workflow:

**Business Issue → Incident Investigation → SQL Analysis → Python Analysis → Root Cause Assessment → Power BI Dashboard → Incident Report**

## Business Problem

A delivery operations team reported potential inconsistencies in delivery event data.

The investigation focused on three types of data quality issues:

* Missing Delivered events
* Duplicate Delivered events
* Invalid event timestamps

The objective was to determine:

* Which hubs were affected
* How frequently incidents occurred
* What types of incidents were most common
* Whether incidents showed recurring patterns over time
* What the potential operational impact was

## Key Findings

* **6,915** orders were marked as Delivered.
* **223** delivered orders at hub **IL01** had missing or duplicate Delivered events.
* IL01 had an **8.06% incident rate** among its 2,768 delivered orders.
* **150** Missing Delivered Event cases were identified.
* **73** Duplicate Delivered Event cases were identified.
* **50** Invalid Event Timestamp cases were identified.
* The other hubs did not show missing or duplicate Delivered-event issues in this dataset.

## Technical Workflow

### 1. Data Generation

Generated a synthetic last-mile delivery dataset containing:

* Orders
* Delivery events
* Hub information

Python was used to generate realistic delivery records and event timestamps.

### 2. Incident Injection

Controlled data quality issues were introduced to simulate real-world support incidents:

* Missing delivery events
* Duplicate delivery events
* Suspicious timestamps

This created a reproducible environment for investigation and troubleshooting.

### 3. SQL Investigation

DuckDB and SQL were used to reconcile order statuses with delivery events.

The investigation identified:

* Missing Delivered events
* Duplicate Delivered events
* Incident rates by hub
* Invalid event timestamps

### 4. Python Investigation

Python and Pandas were used for deeper analysis, including:

* Incident classification
* Hub-level analysis
* Daily incident trends
* Timestamp validation
* Duplicate-event investigation
* Incident overlap analysis

### 5. Power BI Dashboard

The Power BI dashboard provides operational visibility into:

* Total delivered orders
* Incident rate by hub
* Incident types
* Daily incident trends

### 6. Incident Report

The investigation findings were documented in an incident report containing:

* Issue summary
* Investigation approach
* Key findings
* Preliminary root cause assessment
* Operational impact
* Recommended next steps
* Validation plan

## Tools & Technologies

* **SQL / DuckDB**
* **Python**
* **Pandas**
* **NumPy**
* **Power BI**
* **Git / GitHub**

## Project Structure

```text
speedx-data-tech-support/
│
├── data/
│   ├── orders.csv
│   ├── hubs.csv
│   ├── delivery_events.csv
│   ├── delivery_events_incident.csv
│   ├── incident_summary.csv
│   ├── incident_type_summary.csv
│   ├── dashboard_hub_kpi.csv
│   ├── dashboard_incident_type_kpi.csv
│   └── dashboard_daily_incident_kpi.csv
│
├── sql/
│   ├── 01_delivery_event_reconciliation.sql
│   ├── 02_incident_rate.sql
│   └── 03_timestamp_quality.sql
│
├── python/
│   ├── generate_data.py
│   ├── inject_issues.py
│   ├── run_sql.py
│   ├── analyze_incidents.py
│   └── prepare_dashboard_data.py
│
├── dashboard/
│   └── SpeedX_Data_Tech_Support_Dashboard.pbix
│
├── incident_reports/
│   └── IL01_delivery_data_quality_incident.md
│
├── documentation/
│
├── .gitignore
└── README.md
```

## Root Cause Assessment

The analysis identified a clear concentration of delivery-event data quality issues at IL01.

The evidence suggests that the issues were associated with the delivery-event data flow for this hub.

However, the dataset does not contain application logs or system-level telemetry, so an exact technical root cause such as a specific API, database, or application failure cannot be confirmed from the available evidence.

The investigation therefore focuses on evidence-based findings and recommended validation steps rather than assuming an unsupported root cause.

## Recommended Next Steps

1. Validate the Delivered-event ingestion process for IL01.
2. Review application or API logs around affected orders.
3. Check event-generation and event-deduplication logic.
4. Validate timestamp generation and timezone handling.
5. Reconcile affected orders against the source system.
6. Monitor IL01 incident rates after remediation.

## Skills Demonstrated

This project demonstrates practical experience with:

* SQL-based data investigation
* Python/Pandas analysis
* Data quality validation
* Incident investigation
* Root cause analysis
* KPI development
* Power BI dashboarding
* Technical documentation
* Operational reporting
* Data-driven troubleshooting
* Git/GitHub workflow
