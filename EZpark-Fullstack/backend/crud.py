from sqlalchemy.orm import Session
from . import models

def create_item(db: Session, latitude: float, longitude: float):
    db_item = models.Coordinate(latitude=latitude, longitude=longitude)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session):
    return db.query(models.Coordinate).all()
