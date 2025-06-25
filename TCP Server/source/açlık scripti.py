import socket
import time

ip_adress = "127.0.0.1"
with open("Data\\hunger.txt", "r") as file:
    data = file.read().split("\n")
is_enabled = int(data.pop(0).split(" : ")[1])
interval = int(data.pop(0).split(" : ")[1])

while is_enabled:
    time.sleep(interval * 60)
    server = socket.socket()
    server.connect((ip_adress, 80))
    server.send("A /sts%3C13".encode())
    print("Got:  " + server.recv(1024).decode())
    server.close()
input("Hunger is not enabled.")
