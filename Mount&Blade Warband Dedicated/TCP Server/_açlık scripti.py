import socket
import time

ip_adress = "127.0.0.1"

while True:
    time.sleep(180)
    #input()
    server = socket.socket()
    server.connect((ip_adress, 80))
    server.send("A /sts%3C13".encode())
    print("Got:  " + server.recv(1024).decode())
    server.close()
