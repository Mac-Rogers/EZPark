"""
Script to receive GPS coordinates streamed from Android device running QPython script.
Run this server before starting the script on phone. Ensure both devices on same network and change the IP if required
"""
import socket
import ast
import threading
import time

from location import Location

lock = threading.Event()


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
    s.bind((host, port))
    print("Started server")
    s.listen(1)
    client, addr = s.accept()
    print(f"Accepted client at IP address {addr[0]} and port {addr[1]}")

    request_location_thread = threading.Thread(target=request_location, args=(client,))
    request_location_thread.start()

def start_backend_comms():
    backend_comms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    backend_comms.bind(('localhost', 8765))
    backend_comms.listen(5)
    print("Server started on port 8765")

    client_sock, addr = backend_comms.accept()
    print(f"Accepted connection from {addr[0]} on port {addr[1]}")
    while True:
        msg = client_sock.recv(1024).decode()
        if msg == "Request location":
            trigger_request()

def main():
    start_server()
    start_backend_comms()



if __name__ == "__main__":
    main()
