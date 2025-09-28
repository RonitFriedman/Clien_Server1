import socket
import glob
import os
import shutil
import subprocess
import pyautogui

server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 8820))
server_socket.listen()
print("Server is up...")

client_socket, client_address = server_socket.accept()
print("Client connected:", client_address)

while True:
    data_length = client_socket.recv(3).decode()
    if not data_length:
        break

    if int(data_length) < 1 or int(data_length) > 999:
        response = "Unknown command"
    else:
        data = client_socket.recv(int(data_length)).decode()
        comment = data.split()

        if comment[0] == "DIR":
            try:
                if glob.glob(comment[1]) == []:
                    response = "FOLDER NOT FOUND OR THE FOLDER IS EMPTY"
                else:
                    response = str(glob.glob(comment[1]))
            except:
                response = "Not found"
        elif comment[0] == "DELETE":
            try:
                if os.path.exists(comment[1]):
                    os.remove(comment[1])
                    response = f"Deleted {comment[1]}"
            except:
                response = "Not found!"
            else:
                response = f"File {comment[1]} not found"
        elif comment[0] == "COPY":
            try:
                shutil.copy(comment[1], comment[2])
                response = f"Copied {comment[1]} to {comment[2]}"
            except:
                response = f"File {comment[1]} not found or the name of your new file is not valid!"
        elif comment[0] == "EXECUTE":
            try:
                subprocess.call(comment[1])
                response = f"Executed {comment[1]}"
            except:
                response = f"{comment[1]} not found!"

        elif comment[0] == "TAKE_SCREENSHOT":
            try:
                image = pyautogui.screenshot()
                image.save(r"C:\Cyber\screen.jpg")
                response = "Screenshot saved as screen.jpg"
            except:
                response = "Screenshots didn't succeeds"
        elif comment[0] == "PHOTO_SEND":
            try:
                file_path = r"C:\Cyber\screen.jpg"
                if not os.path.exists(file_path):
                    response = "No screenshot found"
                else:
                    file_size = os.path.getsize(file_path)
                    response = "Sent the photo"

                    # שולחים כותרת: 20 לבייטים + 3 להודעה
                    header = str(file_size).ljust(20) + str(len(response)).zfill(3)
                    client_socket.send(header.encode())

                    # שולחים את התמונה
                    with open(file_path, "rb") as f:
                        data = f.read(1024)
                        while data:
                            client_socket.send(data)
                            data = f.read(1024)

                    # שולחים את ההודעה
                    client_socket.send(response.encode())
                    continue  # ממשיכים ללולאה בלי לשלוח שוב message רגיל
            except:
                response = "no photo sent"
        elif comment[0] == "EXIT":
            response = "Bye bye"
            client_socket.send(str(len(response)).zfill(3).encode() + response.encode())
            break
        else:
            response = "Unknown command"

    # בניית הודעה עם אורך 3 ספרות
    length = str(len(response)).zfill(3)
    message = length + response
    client_socket.send(message.encode())

client_socket.close()
server_socket.close()
