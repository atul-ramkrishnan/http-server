class HttpResponse:
    def __init__(self, status_code: int = 200, status_message: str = "OK", body=None, headers: dict = None):
        self.version = "HTTP/1.1"  # Default HTTP version
        self.status_code = status_code
        self.status_message = status_message
        self.headers = headers or {}

        # Ensure the body is in bytes
        if isinstance(body, str):
            self.body = body.encode("utf-8")  # Convert string to bytes
        elif isinstance(body, bytes):
            self.body = body  # Keep bytes as-is
        else:
            raise TypeError("Body must be a string or bytes")

        # Set Content-Length based on byte length
        self.headers["Content-Length"] = str(len(self.body))
        
        # Set default Content-Type if not already provided
        self.headers.setdefault("Content-Type", "text/html; charset=UTF-8")

    def build_response(self):
        # Construct the response line
        response_line = f"{self.version} {self.status_code} {self.status_message}\r\n"

        # Construct the headers
        headers = "".join(f"{key}: {value}\r\n" for key, value in self.headers.items())

        # Combine response line, headers, and body
        return response_line.encode("utf-8") + headers.encode("utf-8") + b"\r\n" + self.body

    def __str__(self):
        # Decode for printing (ignoring binary data for human readability)
        return self.build_response().decode("utf-8", errors="ignore")

# Example Usage:
if __name__ == "__main__":
    # String body
    string_body = "<html><body><h1>Hello, world!</h1></body></html>"
    string_response = HttpResponse(body=string_body)
    
    # When sending, use get_full_response()
    full_response = string_response.get_full_response()
    print(full_response)
    
    # Gzip compressed body example
    import gzip
    compressed_body = gzip.compress(string_body.encode('utf-8'))
    compressed_response = HttpResponse(body=compressed_body, 
                                       headers={'Content-Encoding': 'gzip'})
    full_compressed_response = compressed_response.get_full_response()
    print(full_compressed_response)