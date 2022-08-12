import socket
import time

ip_adress = "127.0.0.1"

while True:
    server = socket.socket()
    server.connect((ip_adress, 80))
    server.send("A /save_to_db".encode())
    print("Got:  " + server.recv(1024).decode())
    server.close()
    time.sleep(20)
