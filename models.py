from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ride(Base):
    __tablename__ = 'rides'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    pickup_location = Column(String)
    destination = Column(String)
    ride_type = Column(String)
    driver_name = Column(String)
    car_details = Column(String)
    estimated_arrival = Column(Integer)  # in minutes
    fare_estimate = Column(String)
    status = Column(String)  # e.g., 'requested', 'driver_assigned', 'on_trip', 'completed'
    timestamp = Column(DateTime)