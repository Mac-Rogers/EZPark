from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from . import models, crud
import requests
from geopy.geocoders import Nominatim

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ItemCreate(BaseModel):
    latitude: float
    longitude: float

def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    db = next(get_db())


@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@app.post("/items/")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    print(f"Received data: {item}")  # Add logging
    return crud.create_item(db, item.latitude, item.longitude)

@app.get("/gps-coordinates")
async def get_gps_coordinates():
    longitude, latitude = get_current_location()
    return {"longitude": latitude, "latitude": longitude} 

@app.post("/clear-db/")
def clear_db(db: Session = Depends(get_db)):
    # Delete all items in the database
    db.query(models.Coordinate).delete()
    db.commit()
    return {"message": "All items have been deleted."}

# Finds network geolocation
def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    return response.json()['ip']

def get_coordinates_from_ip(ip):
    response = requests.get(f'https://ipinfo.io/{ip}/json')
    location = response.json()['loc']
    latitude, longitude = map(float, location.split(','))
    return latitude, longitude

def get_current_location():
    ip = get_public_ip()
    latitude, longitude = get_coordinates_from_ip(ip)
    return latitude, longitude

def initialize_database(db: Session):
    # Add predefined coordinates
    predefined_coords = [
        {"latitude": 40.7128, "longitude": -74.0060},  # New York
        {"latitude": 34.0522, "longitude": -118.2437}, # Los Angeles
        {"latitude": 51.5074, "longitude": -0.1278}    # London
    ]
    for coord in predefined_coords:
        if not crud.item_exists(db, coord["latitude"], coord["longitude"]):
            crud.create_item(db, coord["latitude"], coord["longitude"])
