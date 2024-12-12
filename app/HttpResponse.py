class HttpResponse:
    def __init__(self, status_code: int = 200, status_message: str = "OK", body: str | bytes = "", headers: dict = None):
        self.version = "HTTP/1.1"  # Default HTTP version
        self.status_code = status_code
        self.status_message = status_message
        self.headers = headers or {}
        
        # Normalize body to bytes if it's a string
        self.body = body.encode('utf-8') if isinstance(body, str) else body
        
        # Set Content-Length based on byte length
        self.headers["Content-Length"] = str(len(self.body))
        self.headers.setdefault("Content-Type", "text/html; charset=UTF-8")  # Default content type
    
    def build_response(self):
        # Construct the response line
        response_line = f"{self.version} {self.status_code} {self.status_message}\r\n"
        
        # Construct the headers
        headers = ""
        for key, value in self.headers.items():
            headers += f"{key}: {value}\r\n"
        
        # Combine response line, headers, and body
        # Ensure everything is converted to bytes
        full_response = (response_line + headers + "\r\n").encode('utf-8') + self.body
        
        return full_response
    
    def __str__(self):
        # Attempt to decode the response if possible
        try:
            return self.build_response().decode('utf-8')
        except UnicodeDecodeError:
            # If decoding fails (e.g., for binary data), return a byte representation
            return str(self.build_response())

# Example Usage:
if __name__ == "__main__":
    # String body
    string_body = "<html><body><h1>Hello, world!</h1></body></html>"
    string_response = HttpResponse(body=string_body)
    print("String Body Response:")
    print(string_response)
    
    # Bytes body (e.g., compressed or binary content)
    bytes_body = b"Some compressed or binary content"
    bytes_response = HttpResponse(body=bytes_body)
    print("\nBytes Body Response:")
    print(bytes_response)
    
    # Gzip compressed body example
    import gzip
    compressed_body = gzip.compress(string_body.encode('utf-8'))
    compressed_response = HttpResponse(body=compressed_body, 
                                       headers={'Content-Encoding': 'gzip'})
    print("\nCompressed Body Response:")
    print(compressed_response)