import socket

file = open("basic_settings.txt", "r+")
database = file.read().split("\n")
file.close()
ip_adress = database[7].split(" : ")[1]

password = input("Admin pass: ")

connect = True

while True:
    try:
        if connect:
            server = socket.socket()
            server.connect((ip_adress, 22161))
            server.send("A /admin_connect%3C{}".format(password).encode())
        message = server.recv(1024).decode()
        if message == "%reconnect%":
            server.close()
            connect = True
        else:
            print(message)
            connect = False
    except Exception:
        connect = True
        continue
