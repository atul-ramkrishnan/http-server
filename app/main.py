import socket
import threading
import argparse
import os

def handle_client(connection, args):
    status_line = ""
    headers = ""
    response_body = ""
    data = connection.recv(1024).decode() # receive data
    method = data.split()[0] # get method from request
    path = data.split()[1] # get path from request
    if method == "GET":
        if path == "/":
            status_line = 'HTTP/1.1 200 OK\r\n'
            headers = "Content-Type: text/html\r\n"
        elif path.startswith("/echo"):
            status_line = 'HTTP/1.1 200 OK\r\n'
            response_body = path.split("/echo/")[1]
            headers = f"Content-Type: text/plain\r\nContent-Length: {len(response_body)}\r\n"
        elif path.startswith("/file"):
            file_path = args.directory + path.split("/files")[1]
            try:
                with open(file_path, "r") as file:
                    status_line = 'HTTP/1.1 200 OK\r\n'
                    response_body = file.read()
                    headers = f"Content-Type: application/octet-stream\r\nContent-Length: {os.path.getsize(file_path)}\r\n"
            except FileNotFoundError:
                status_line = 'HTTP/1.1 404 Not Found\r\n'
        elif path == "/user-agent":
            status_line = 'HTTP/1.1 200 OK\r\n'
            response_body = data.split("User-Agent: ")[1].split("\r\n")[0]
            headers = f"Content-Type: text/plain\r\nContent-Length: {len(response_body)}\r\n"            
        else:
            status_line = 'HTTP/1.1 404 Not Found\r\n'
        
    elif method == 'POST':
        if path.startswith("/files"):
            file_path = args.directory + path.split("/files")[1]
            header_section, body = data.split('\r\n\r\n', 1)
            with open(file_path, 'w') as file:
                file.write(body)
            status_line = 'HTTP/1.1 201 Created\r\n'
    else:
        status_line = 'HTTP/1.1 405 Method Not Allowed\r\n'

    response = status_line + headers + "\r\n" + response_body
    connection.sendall(response.encode())
    connection.close()
def main():
    print("Server is running on localhost:4221")
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str, default=".")
    args = parser.parse_args()
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    try:
        while True:
            connection, address = server_socket.accept() # wait for client
            client_thread = threading.Thread(target=handle_client, args=(connection, args))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down")
        server_socket.close()
if __name__ == "__main__":
    main()
