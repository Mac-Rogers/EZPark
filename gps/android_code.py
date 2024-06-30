"""
Script to run with QPython ON ANDROID PHONE!!!
Gets GPS coordinates and streams to the server running on laptop.
"""
import android
import time
import socket
port = 12345
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("192.168.185.84", port))  # Ip address of the connected network
print("Connected to server")
droid = android.Android()
while True:
    droid.startLocating(1000, 1, False)  # Min update time, min update distance and gnss
    droid.eventWaitFor('location', int(9000))
    location = droid.readLocation().result
    if not location:
        print("\n\n NO LOCATION \n\n")
    print(location)
    data = bytes(str(location),'ascii')
    try:
        s.send(data)
    except (BrokenPipeError, ConnectionResetError):
        print("Server closed")
        break
    time.sleep(3)
s.close()
droid.stopLocating()
