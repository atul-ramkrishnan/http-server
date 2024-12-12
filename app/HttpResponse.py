class HttpResponse:
    def __init__(self, status_code: int = 200, status_message: str = "OK", body: str = "", headers: dict = None):
        self.version = "HTTP/1.1"  # Default HTTP version
        self.status_code = status_code
        self.status_message = status_message
        self.headers = headers or {}
        self.body = body
        self.headers["Content-Length"] = str(len(body))  # Set the Content-Length header by default
        self.headers.setdefault("Content-Type", "text/html; charset=UTF-8")  # Default content type

    def build_response(self):
        # Construct the response line
        response_line = f"{self.version} {self.status_code} {self.status_message}\r\n"

        # Construct the headers
        headers = ""
        for key, value in self.headers.items():
            headers += f"{key}: {value}\r\n"

        # Combine response line, headers, and body
        return response_line + headers + "\r\n" + self.body

    def __str__(self):
        return self.build_response()

# Example Usage:
if __name__ == "__main__":
    # Example of creating an HTTP Response
    body = "<html><body><h1>Hello, world!</h1></body></html>"
    response = HttpResponse(status_code=200, status_message="OK", body=body)
    
    # Print the generated response
    print(response)