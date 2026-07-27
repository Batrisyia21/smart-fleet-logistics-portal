# Smart Fleet & Logistics Optimization Portal
Live Demo: https://smart-fleet-logistics-app-cavlv4ojzfe36eypvcsp39.streamlit.app/

An interactive, web-based fleet management and telemetry analytics portal developed with Python, Streamlit, and SQLite. Built for the BIT1034 Advanced Programming group project.

## Project Overview

Modern logistics operators often struggle with fragmented telemetry data and complex database interactions. This portal bridges the gap by providing a seamless visual interface that combines real-time operational analytics, direct SQLite CRUD management, spatial GPS tracking, and database transparency into a single web application.

##  Core Features

- Executive Analytics Dashboard (Performance Hub): Real-time operational dashboard with dynamic KPI cards tracking total trips, delayed shipments, average utilization, and waiting times. Includes categorical breakdowns for status and delay factors.
- Dispatch Control Console (CRUD Operations): Interactive forms that allow dispatchers to safely register new shipments (`INSERT`) and update live record statuses (`UPDATE`) directly within the SQLite database using parameterized queries.
- Global GPS & Fleet Tracker: Spatial visualization powered by coordinate normalization algorithms mapping fleet positions across 11 major international land logistics hubs.
- Live Database Records Inspection: A transparent, interactive data grid displaying the full `fleet_shipments` table from `logistics_system.db`.

##  Tech Stack & Requirements

- Programming Language: Python 3.x
- Web Framework: Streamlit
- Database Management: SQLite3
- Data Analysis & Processing: Pandas

##  Repository Structure

```text
├── app.py                      # Main Streamlit application codebase
├── smart_logistics_dataset.csv # Raw input logistics CSV dataset
├── logistics_system.db         # Relational SQLite database
├── requirements.txt            # External Python dependencies
└── README.md                   # Repository documentation


##  Authors

Developed as a group project for BIT1034 Advanced Programming:

Student 1 Name - Nur Batrisyia Binti Zool Hilmi (B24090012)

Student 2 Name - Aina Safirah Binti Saifuddin (B24090022)
