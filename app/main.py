import socket  # noqa: F401

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        connection, address = server_socket.accept() # wait for client
        status_line = ""
        headers = ""
        response_body = ""
        data = connection.recv(1024).decode() # receive data
        path = data.split()[1] # get path from request

        if path == "/":
            status_line = 'HTTP/1.1 200 OK\r\n'
            headers = "Content-Type: text/html\r\n"
        elif path.startswith("/echo"):
            status_line = 'HTTP/1.1 200 OK\r\n'
            response_body = path.split("/echo/")[1]
            headers = f"Content-Type: text/plain\r\nContent-Length: {len(response_body)}\r\n"
        else:
            # connection.sendall('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
            status_line = 'HTTP/1.1 404 Not Found\r\n'
        response = status_line + headers + "\r\n" + response_body
        connection.sendall(response.encode())
        connection.close()

if __name__ == "__main__":
    main()
