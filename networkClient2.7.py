import os
import socket

my_socket = socket.socket()
my_socket.connect(('127.0.0.1', 8820))

while True:
    msg = input("Enter command (DIR / DELETE / COPY / EXECUTE / TAKE_SCREENSHOT / PHOTO_SEND / EXIT): ")

    length = str(len(msg)).zfill(3)
    message = length + msg
    my_socket.send(message.encode())

    if msg == "PHOTO_SEND":
        # מקבלים כותרת: 20 לבייטים + 3 להודעה
        header = my_socket.recv(23).decode()
        file_size = int(header[:20].strip())
        resp_len = int(header[20:])

        print("Receiving photo of size:", file_size, "bytes")

        # מורידים את התמונה
        received = 0
        file_name = "received.jpg"
        with open(file_name, "wb") as f:
            while received < file_size:
                data = my_socket.recv(1024)
                if not data:
                    break
                f.write(data)
                received += len(data)

        print("Photo saved as received.jpg")

        os.startfile(file_name)

        # מקבלים את ההודעה
        response = my_socket.recv(resp_len).decode()
        print("Server:", response)
        continue  # ממשיכים ללולאה בלי לשלוח שוב message רגיל
    else:
        data_length = int(my_socket.recv(3).decode())
        response = my_socket.recv(data_length).decode()
        print("Server:", response)
    if msg == "EXIT":
        break

my_socket.close()
