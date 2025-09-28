import datetime
import socket
import random
import glob

server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 8820))
server_socket.listen()
print("Server is up...")

(client_socket, client_address) = server_socket.accept()
print("Client connected:", client_address)

while True:

    data_length = client_socket.recv(3).decode()
    if int(data_length) < 1 or int(data_length) > 999:
        response = "Unknown command"
        # בניית ההודעה עם אורך 3 ספרות
        length = str(len(response))
        zfill_length = length.zfill(3)
        message = zfill_length + response

        client_socket.send(message.encode())
        continue

    if not data_length:  # אם הלקוח סגר את החיבור
        break

    data = client_socket.recv(int(data_length)).decode()
    if not data:
        break

    if data == "TIME":
        response = str(datetime.date.today())
    elif data == "WHORU":
        response = "I'm Harel's girlfriend"
    elif data == "RAND":
        response = str(random.randint(1, 10))
    elif data == "EXIT":
        response = "Bye bye"
        # שולחים את ההודעה וסוגרים
        length = str(len(response))
        zfill_length = length.zfill(3)
        message = zfill_length + response
        client_socket.send(message.encode())
        break
    else:
        response = "Unknown command"

    # בניית ההודעה עם אורך 3 ספרות
    length = str(len(response))
    zfill_length = length.zfill(3)
    message = zfill_length + response

    client_socket.send(message.encode())

client_socket.close()
server_socket.close()
