import socket
import sqlite3

connection_sql = sqlite3.connect('test.db')

close = False
while close == False:
    new_socket = socket.socket() # default values: socket.AF_INET, socket.SOCK_STREAM, and socket.IPPROTO_TCP
    port = ("localhost", 8080 )
    new_socket.bind(port)
    new_socket.listen()
    #print(f"new_socket: {new_socket}\n")
    
    client = new_socket.accept()
    #print(f"client: {client}\n")
    client_address = client[1]
    client_object = client[0]
    client_message = client_object.recv(4096).decode('utf-8')
    if client_message == "close":
        close = True
    else:
        #print(f"<type of the received message: {type(client_message)}>")
        client_message_by_line = client_message.splitlines()
        
        # for line in client_message_by_line:
        #     print(f"{line}")
        
        http_request_method = client_message_by_line[0].split()[0]
        http_request_url = client_message_by_line[0].split()[1]
        http_protocol_version = client_message_by_line[0].split()[2]
        #print(f"\n{http_request_method}\n {http_request_url}\n{http_protocol_version}")
        
        status_code = None
        response_file = None
        if http_request_method == "GET":
            try:
                with open(http_request_url[1:], 'r') as file:
                    response_file = file.read()
                status_code = "200 OK"
            except Exception:
                status_code = "404 Not Found"
                print(client_message_by_line[0])
                pass
        elif http_request_method == "POST":
            print(client_message)
            values = client_message_by_line[-1].split('&')
            username = values[0].split('=')[1]
            password = values[1].split('=')[1]
            print(f"{[value for value in values]}")
            print(f"username= {username} password= {password}")
            connection_sql.execute("INSERT INTO test (username, password) VALUES (?, ?)", (username, password))
        else:
            print(client_message_by_line)

        response_headers = ("Content-Type: text/html")
        response_message = (
            f"{http_protocol_version} {status_code}\n{response_headers or ''}\n\n{response_file or ''}"
        )
        client_object.send(response_message.encode("utf-8"))

    client_object.close()

connection_sql.commit()
connection_sql.close()