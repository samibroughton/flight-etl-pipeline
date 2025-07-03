import requests
import json
from datetime import datetime
from pathlib import Path
from minio import Minio

class FlightState:
    def __init__(self, state_array, timestamp):
        self.icao24 = state_array[0]
        self.callsign = state_array[1].strip() if state_array[1] else None
        self.origin_country = state_array[2]
        self.last_position_update = self._convert_unix(state_array[3])
        self.last_contact = self._convert_unix(state_array[4])
        self.longitude = state_array[5]
        self.latitude = state_array[6]
        self.on_ground = state_array[8]
        self.timestamp = self._convert_unix(timestamp)

    def _convert_unix(self, ts):
        return datetime.utcfromtimestamp(ts) if ts else None

    def _serialize_datetime(self, dt):
        return dt.isoformat() if dt else None

    def to_dict(self):
        return {
            "icao24": self.icao24,
            "callsign": self.callsign,
            "origin_country": self.origin_country,
            "last_position_update": self._serialize_datetime(self.last_position_update),
            "last_contact": self._serialize_datetime(self.last_contact),
            "longitude": self.longitude,
            "latitude": self.latitude,
            "on_ground": self.on_ground,
            "timestamp": self._serialize_datetime(self.timestamp),
        }


def fetch_opensky_data():
    url = "https://opensky-network.org/api/states/all"
    headers = {
        "User-Agent": "flight-etl/1.0"  
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise ValueError(f"Request failed with status {response.status_code}")

    data = response.json()
    timestamp = data.get("time")
    states = data.get("states")

    return timestamp, states


def clean_results(timestamp, states):
    flight_objects = []
    for s in states:
        if s[5] is not None and s[6] is not None:  # longitude, latitude
            flight = FlightState(s, timestamp)
            flight_objects.append(flight)
    return flight_objects

def save_to_json(flight_objects, output_dir="data/raw"):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
    filename = f"opensky_{timestamp}.json"
    filepath = Path(output_dir) / filename

    data = [f.to_dict() for f in flight_objects]

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    return filepath


def upload_to_minio(filepath, bucket="opensky"):
    # 1. Connect to MinIO (localhost:9000)
    client = Minio(
        "localhost:9000",                     # host:port combo as a string
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    # 2. Ensure the bucket exists
    if not client.bucket_exists(bucket):     # <-- method is bucket_exists()
        client.make_bucket(bucket)

    # 3. Upload the file
    object_name = Path(filepath).name        # just the filename, not full path
    client.fput_object(
        bucket,
        object_name,
        filepath,
        content_type="application/json"
    )

def main():
    timestamp, states = fetch_opensky_data()
    flight_objects = clean_results(timestamp, states)
    filepath = save_to_json(flight_objects)
    upload_to_minio(filepath)

if __name__ == "__main__":
    main()
