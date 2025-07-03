# ✈️ Flight ETL Pipeline

A fully modular, production-style ETL pipeline for real-time global flight tracking data — built from scratch using Python, PostgreSQL, MinIO, and dbt.

This project scrapes live data from the OpenSky Network API, cleans and stores it, and models insightful analytics with dbt. It's the backbone of a data platform that could power dashboards, anomaly detection, or even your own FlightRadar clone.

---

## 📦 Tech Stack

- **Python**: API ingestion, transformation, and orchestration
- **MinIO**: Object storage (S3-compatible)
- **PostgreSQL**: Analytical warehouse
- **SQLAlchemy**: ORM for structured inserts
- **dbt**: Data modeling and testing
- **Docker**: Local development environment

---

## 🔁 ETL Flow

1. **Ingest**: Pulls flight data from OpenSky REST API as raw JSON.
2. **Transform**: Cleans nulls, standardizes timestamps, and extracts fields into Python class objects.
3. **Store**:
   - Writes raw JSON to MinIO
   - Inserts structured rows into PostgreSQL
4. **Model (dbt)**:
   - Stages the raw data
   - Builds fact and dimension tables
   - Tests for nulls, accepted values, and business logic

---

## 🚀 Getting Started

```bash
git clone https://github.com/samibroughton/flight-etl-pipeline.git
cd flight-etl-pipeline
```

## Start the environment:
docker-compose up -d
Install Python dependencies:
pip install -r requirements.txt

## Run the ETL pipeline:
python main_etl.py

## Run dbt models:
cd flight_dbt
dbt run

## 📊 Models Included

stg_flights: Staged source of raw flight data
fct_active_flights: Fact table tracking daily flight volume
dim_airports: (stretch goal) Dimension table joining airport metadata
✅ Testing (dbt)

dbt test

Tests include:

Not null constraints
Accepted value ranges
Custom expectation logic

## ✨ Why This Matters

This pipeline is a fully modular foundation for building data platforms, real-time analytics, and custom dashboards. It demonstrates mastery across the full modern data stack — from ingestion to modeling to orchestration.

## 🛠️ Contributions

Contributions, feature ideas, and pull requests are warmly welcomed. See CONTRIBUTING.md for more.

## 📜 License

MIT — see LICENSE for details.

