"""
Script to receive GPS coordinates streamed from Android device running QPython script.
Run this server before starting the script on phone. Ensure both devices on same network and change the IP if required
"""
import socket
import ast
s = socket.socket()
# Change this IP if needed
host = '192.168.185.84'
port = 12345
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
print("Started server")
s.listen(1)
message, addr = s.accept()
while True:
    location_raw = message.recv(2048).decode('ascii')
    if not location_raw:
        print("Client closed connection")
        break
    location = ast.literal_eval(location_raw)  # Get dictionary object
    # Determine the mode with the highest accuracy and use that
    accuracy_list = {}
    for mode in location:
        accuracy_list.update({mode: location.get(mode).get('accuracy')})
    data_mode = min(accuracy_list, key=accuracy_list.get)
    data = location.get(data_mode, {})

    # Make sure it isn't an empty position
    if data:
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        accuracy = data.get('accuracy')
        provider = data.get('provider')
        print(f"{provider} - Latitude, Longitude: {latitude}, {longitude}, Accuracy: {accuracy}")
    else:
        print("No location data received")
