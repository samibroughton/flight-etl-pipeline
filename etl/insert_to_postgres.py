from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy_flightrecord import Base, FlightRecord

def insert_flights_to_postgres(flight_objects):
    # 1. Setup engine
    engine = create_engine("postgresql://flightuser:flightpass@localhost:5432/flightdata")


    # 2. Create tables
    Base.metadata.create_all(engine)

    # 3. Insert data
    Session = sessionmaker(bind=engine)
    session = Session()

    records = [FlightRecord(**f.to_dict()) for f in flight_objects]
    try:
        session.bulk_save_objects(records)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"DB insert failed: {e}")
    finally:
        session.close()

    return len(records)

if __name__ == "__main__":
    from etl.fetch_opensky import fetch_opensky_data, clean_results

    # 1. Fetch and clean
    timestamp, states = fetch_opensky_data()
    flight_objects = clean_results(timestamp, states)

    # 2. Insert into Postgres
    inserted_count = insert_flights_to_postgres(flight_objects)
    print(f"✅ Inserted {inserted_count} flights into Postgres")
