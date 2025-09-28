import socket

# יצירת סוקט לשרת
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8820))  # מאזין על כל הכתובות המקומיות בפורט 8820
server_socket.listen(1)

print("Echo Server is up and running...")

(client_socket, client_address) = server_socket.accept()
print("Client connected from:", client_address)

# קבלת הודעה מהלקוח
data = client_socket.recv(1024).decode()
print("Client sent:", data)

# החזרת ההודעה ללקוח
client_socket.send(data.encode())
print("Echoed back to client:", data)

# סגירת חיבורים
client_socket.close()
server_socket.close()
