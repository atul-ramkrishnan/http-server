import socket
import threading


def handle_client(connection):
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
    elif path == "/user-agent":
        status_line = 'HTTP/1.1 200 OK\r\n'
        response_body = data.split("User-Agent: ")[1].split("\r\n")[0]
        headers = f"Content-Type: text/plain\r\nContent-Length: {len(response_body)}\r\n"            
    else:
        status_line = 'HTTP/1.1 404 Not Found\r\n'
    response = status_line + headers + "\r\n" + response_body
    connection.sendall(response.encode())
    connection.close()

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        connection, address = server_socket.accept() # wait for client
        client_thread = threading.Thread(target=handle_client, args=(connection, ))
        client_thread.start()

if __name__ == "__main__":
    main()
