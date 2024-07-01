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
    name: str

def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@app.post("/items/")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item.name)

@app.get("/gps-coordinates")
async def get_gps_coordinates():
    longitude, latitude = get_current_location()
    return {"longitude": latitude, "latitude": longitude} 

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
