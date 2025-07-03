from etl.fetch_opensky import fetch_opensky_data, clean_results, save_to_json, upload_to_minio
from insert_to_postgres import insert_flights_to_postgres

def main():
    print("🚀 Starting ETL pipeline...")

    timestamp, states = fetch_opensky_data()
    print(f"📡 Fetched {len(states)} states at {timestamp}")

    flight_objects = clean_results(timestamp, states)
    print(f"🧼 Cleaned to {len(flight_objects)} valid flight objects")

    filepath = save_to_json(flight_objects)
    print(f"💾 Saved raw JSON to {filepath}")

    upload_to_minio(filepath)
    print(f"📤 Uploaded file to MinIO bucket")

    inserted = insert_flights_to_postgres(flight_objects)
    print(f"📥 Inserted {inserted} records into PostgreSQL")

    print("✅ ETL pipeline completed!")

if __name__ == "__main__":
    main()