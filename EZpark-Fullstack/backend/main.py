from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from . import models, crud
import requests

import threading
import socket
import ast
from .location import Location
import time

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

# Lock used in multithreading
lock = threading.Event()

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


def parse_location(location_raw: str) -> dict:
    """
    Many other useful fields returned by location data, which is why a dictionary is used.
    Parse the location from received string and return the data that is most accurate in a dictionary
    :param location_raw:
    :return data: A dictionary with all fields returned by phone GPS
    """
    location_dict = ast.literal_eval(location_raw)  # Get dictionary object
    # Determine the mode with the highest accuracy and use that
    accuracy_list = {}
    for mode in location_dict:
        accuracy_list.update({mode: location_dict.get(mode).get('accuracy')})
    data_mode = min(accuracy_list, key=accuracy_list.get)
    data = location_dict.get(data_mode, {})
    return data


def trigger_request() -> None:
    lock.set()


def request_location(client: socket.socket):
    while True:
        lock.wait()
        client.send("Location Request".encode())
        packet = client.recv(2048)
        location_raw = packet.decode('ascii')
        if not location_raw:
            print("Client closed connection")
            break
        data = parse_location(location_raw)

        # Make sure it isn't an empty position
        if data:
            currentLocation = Location(data.get('latitude'),
                                       data.get('longitude'),
                                       data.get('accuracy'),
                                       data.get('provider'))
            print(currentLocation)

            # Send this currentLocation somewhere to backend?

        else:
            print("No location data received")
        lock.clear()


def start_server():
    s = socket.socket()
    # Change this IP if needed
    host = '192.168.185.84'
    port = 12345
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while True:
        try:
            s.bind((host, port))
            break
        except OSError:
            print("Cannot connect to client. Consider using same network.")
            time.sleep(10)
    print("Started server")
    s.listen(1)
    client, addr = s.accept()
    print(f"Accepted client at IP address {addr[0]} and port {addr[1]}")

    request_location_thread = threading.Thread(target=request_location, args=(client,))
    request_location_thread.start()



# Start the server
# start_server() # Maybe put on a thread


