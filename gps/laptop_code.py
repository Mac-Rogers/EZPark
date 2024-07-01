"""
Script to receive GPS coordinates streamed from Android device running QPython script.
Run this server before starting the script on phone. Ensure both devices on same network and change the IP if required
"""
import socket
import ast
import threading

from location import Location

currentLocation = None


def parse_location(location_raw: str) -> dict:
    """
    Many other useful fields returned by location data, which is why a dictionary is used.
    Parse the location from received string and return the data that is most accurate in a dictionary
    :param location_raw:
    :return:
    """
    location_dict = ast.literal_eval(location_raw)  # Get dictionary object
    # Determine the mode with the highest accuracy and use that
    accuracy_list = {}
    for mode in location_dict:
        accuracy_list.update({mode: location_dict.get(mode).get('accuracy')})
    data_mode = min(accuracy_list, key=accuracy_list.get)
    data = location_dict.get(data_mode, {})
    return data


def request_location(client: socket.socket) -> (float, float, float):
    pass


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

    while True:
        packet = client.recv(2048)
        location_raw = packet.decode('ascii')
        if not location_raw:
            print("Client closed connection")
            break
        data = parse_location(location_raw)

        # Make sure it isn't an empty position
        if data:
            global currentLocation
            currentLocation = Location(data.get('latitude'),
                                       data.get('longitude'),
                                       data.get('accuracy'),
                                       data.get('provider'))
            print(currentLocation)
        else:
            print("No location data received")


def main():
    start_server()


if __name__ == "__main__":
    main()
