from fastapi import FastAPI, Depends, HTTPException
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
import cv2
from geopy.geocoders import Nominatim
from ultralytics import YOLO
import numpy as np

app = FastAPI()
detection_threadhold = 0.75

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
    latitude: float
    longitude: float

class Coordinates(BaseModel):
    end: list[float]

def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

dest_coords = [0, 0]
current_coords = [0,0]

@app.post("/set-coordinates")
async def set_coordinates(end_coords: Coordinates):
    global dest_coords
    dest_coords = end_coords.end
    return {"message": "Coordinates received"}

@app.get("/get-coordinates")
async def get_coordinates():
    global dest_coords
    return {"dest_coords": dest_coords}

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
        global current_coords
        if not location_raw:
            print("Phone disconnected")
            lock.clear()
            client.close()
            break
        data = parse_location(location_raw)

        # Make sure it isn't an empty position
        if data:
            currentLocation = Location(data.get('latitude'),
                                       data.get('longitude'),
                                       data.get('accuracy'),
                                       data.get('provider'))
            print(currentLocation)
            current_coords = [currentLocation.latitude, currentLocation.longitude]

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
            print(f"Unable to start server at {host} on port {port}. Consider using same network as phone.")
            time.sleep(10)
    print(f"Started server at {host} on port {port}")
    while True:
        s.listen(1)
        client, addr = s.accept()
        print(f"Accepted client at IP address {addr[0]} and port {addr[1]}")

        request_location_thread = threading.Thread(target=request_location, args=(client,))
        request_location_thread.start()

def apply_perspective_transform(input_image, scale):
    height, width = input_image.shape[:2]

    # Define the four points in the source image
    pts_src = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)

    # Define the four points in the destination image
    pts_dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1 - scale * 100, height - 1],
        [scale * 100, height - 1]
    ], dtype=np.float32)

    # Calculate the perspective transform matrix
    matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

    # Apply the perspective transformation
    result = cv2.warpPerspective(input_image, matrix, (width, height))

    return result

def apply_binary_threshold(image, threshold):
    # Apply binary thresholding
    _, black_and_white_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return black_and_white_image

def process_webcam_feed(scale=2.7, threshold=200):
    # Load the YOLOv8 model
    model = YOLO('backend/model_weights.pt')

    # Capture video from the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame from webcam.")
            break

        # Convert to grayscale before applying threshold
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply binary thresholding
        black_and_white_image = apply_binary_threshold(gray_image, threshold=threshold)

        # Apply perspective transform
        transformed_image = apply_perspective_transform(black_and_white_image, scale=scale)

        # Convert the transformed image back to BGR
        transformed_image_bgr = cv2.cvtColor(transformed_image, cv2.COLOR_GRAY2BGR)

        # Run YOLOv8 inference on the transformed image
        results = model(transformed_image_bgr)
        #print("Results ",len(results[0].obb.conf.tolist()))
        if len(results[0].obb.conf.tolist()):
            if max(results[0].obb.conf.tolist()) > detection_threadhold:
                trigger_request() #requests coordinates
                time.sleep(0.1)
                db = next(get_db())
                crud.create_item(db, current_coords[0], current_coords[1])
                print("Park Detected!")
                

        # Visualize the results on the transformed image
        annotated_frame = results[0].plot()

        # Display the original and processed frames
        cv2.imshow('Original', frame)
        cv2.imshow('Processed', annotated_frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

#@app.post("/start-webcam")
def start_webcam():
    threading.Thread(target=process_webcam_feed, daemon=True).start()
    return {"message": "Webcam streaming started"}

#@app.post("/start-gps")
def start_gps():
    threading.Thread(target=start_server).start()
    return {"message": "GPS streaming started"}

start_webcam()
start_gps()

# Start the socket server communicating with phone on its own thread
# threading.Thread(target=start_server).start()

