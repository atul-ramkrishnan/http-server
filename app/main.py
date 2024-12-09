import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        connection, address = server_socket.accept() # wait for client
        data = connection.recv(1024).decode() # receive data
        path = data.split()[1] # get path from request
        if path == "/":
            connection.sendall('HTTP/1.1 200 OK\r\n\r\n'.encode())
        else:
            connection.sendall('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
        connection.close()

if __name__ == "__main__":
    main()
