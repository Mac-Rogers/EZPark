from sqlalchemy.orm import Session
from . import models

def get_items(db: Session):
    return db.query(models.Item).all()

def create_item(db: Session, name: str):
    db_item = models.Item(name=name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
