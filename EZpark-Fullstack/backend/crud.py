from sqlalchemy.orm import Session
from . import models
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def create_item(db: Session, latitude: float, longitude: float):
    # Check if any item is within 3 meters of the given coordinates
    all_items = db.query(models.Coordinate).all()
    for item in all_items:
        distance = haversine(latitude, longitude, item.latitude, item.longitude)
        if distance <= 1:  # Distance in meters
            return item
    
    # If no item is within 3 meters, create and add the new item
    db_item = models.Coordinate(latitude=latitude, longitude=longitude)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session):
    return db.query(models.Coordinate).all()
