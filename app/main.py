import socket
import threading
import argparse
import os
from .HttpRequest import HttpRequest
from .HttpResponse import HttpResponse


def handle_get_request(request, args):
    response_headers = {}
    if request.headers.get("Accept-Encoding", "") == "gzip":
        response_headers["Content-Encoding"] = "gzip"
    response = None
    if request.path == "/":
        response_headers["Content-Type"] = "text/html"
        response = HttpResponse(status_code=200,
                                status_message="OK",
                                headers=response_headers)
    elif request.path.startswith("/echo"):
        responseBody = request.path.split("/echo/")[1]
        response_headers["Content-Type"] = "text/plain"
        response_headers["Content-Length"] = str(len(responseBody))
        response = HttpResponse(status_code=200,
                                status_message="OK",
                                body=responseBody,
                                headers=response_headers)
    elif request.path.startswith("/files"):
        filePath = args.directory + request.path.split("/files")[1]
        try:
            with open(filePath, "r") as file:
                responseBody = file.read()
                response_headers["Content-Type"] = "application/octet-stream"
                response_headers["Content-Length"] = str(os.path.getsize(filePath))
                response = HttpResponse(status_code=200,
                                        status_message="OK",
                                        body=responseBody,
                                        headers=response_headers)
        except FileNotFoundError:
            response = HttpResponse(status_code=404,
                                    status_message="Not Found")
    elif request.path == "/user-agent":
        userAgent = request.headers.get("User-Agent", "")
        response_headers["Content-Type"] = "text/plain"
        response_headers["Content-Length"] = str(len(userAgent))
        response = HttpResponse(status_code=200,
                                status_message="OK",
                                body=userAgent,
                                headers=response_headers)
    else:
        response = HttpResponse(status_code=404,
                                status_message="Not Found")
    return response


def handle_post_request(request, args):
    response = None
    if request.path.startswith("/files"):
        filePath = args.directory + request.path.split("/files")[1]
        with open(filePath, "w") as file:
            file.write(request.body)
        response = HttpResponse(status_code=201,
                                status_message="Created")
    else:
        response = HttpResponse(status_code=404,
                                status_message="Not Found")
    return response


def handle_method_not_allowed(connection, request, args):
    response = HttpResponse(status_code=405, status_message="Method Not Allowed")
    return response


def handle_request(connection, request, args):
    response = None
    if request.method == 'GET':
        response = handle_get_request(request, args)
    elif request.method == 'POST':
        response = handle_post_request(request, args)
    else:
        response = handle_method_not_allowed(request, args)
    
    connection.sendall(str(response).encode())
    connection.close()


def handle_client(connection, args):
    data = connection.recv(1024).decode() # receive data
    request = HttpRequest(data)
    print(request)

    return handle_request(connection, request, args)


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
