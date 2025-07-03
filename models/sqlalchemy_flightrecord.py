from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime

Base = declarative_base()

class FlightRecord(Base):
    __tablename__ = "raw_flights"
    id = Column(Integer, primary_key=True, autoincrement=True) 
    icao24 = Column(String)
    callsign = Column(String)
    origin_country = Column(String)
    last_position_update = Column(DateTime)
    last_contact = Column(DateTime)
    longitude = Column(Float)
    latitude = Column(Float)
    on_ground = Column(Boolean)
    timestamp = Column(DateTime)
