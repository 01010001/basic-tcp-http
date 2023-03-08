import socket

client_socket = socket.socket()

address = ("localhost",8080)

client_socket.connect(address)

a = input()

# send to shut the server down
message = "close"

client_socket.send(message.encode('utf-8'))

print(client_socket.recv(4096).decode("utf-8"))

client_socket.close()