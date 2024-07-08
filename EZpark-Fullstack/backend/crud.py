from sqlalchemy.orm import Session
from . import models

def create_item(db: Session, latitude: float, longitude: float):
    # Check if the item already exists
    existing_item = db.query(models.Coordinate).filter_by(latitude=latitude, longitude=longitude).first()
    if existing_item:
        return existing_item
    
    # If the item doesn't exist, create and add it
    db_item = models.Coordinate(latitude=latitude, longitude=longitude)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session):
    return db.query(models.Coordinate).all()
