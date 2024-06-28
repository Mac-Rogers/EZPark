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
    location = ast.literal_eval(location_raw)
    fused_data = location.get('fused', {})
    gps_data = location.get('gps', {})
    network_data = location.get('network', {})
    # Take fused data if available, otherwise gps and network data in that order
    data = fused_data if fused_data else gps_data if gps_data else network_data

    # Make sure it isn't an empty position
    if data:
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        accuracy = data.get('accuracy')
        provider = data.get('provider')
        print(f"{provider} - Latitude: {latitude}, Longitude: {longitude}, Accuracy: {accuracy}")
    else:
        print("No location data received")
