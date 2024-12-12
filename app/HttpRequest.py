class HttpRequest:
    def __init__(self, data: str):
        self.data = data
        self.method = None
        self.path = None
        self.version = None
        self.headers = {}
        self.body = None
        self.parse_request()

    def parse_request(self):
        # Split the request into lines
        lines = self.data.split("\r\n")
        
        # Request line (method, path, version)
        request_line = lines[0].split(" ")
        self.method = request_line[0]
        self.path = request_line[1]
        self.version = request_line[2]
        
        # Parse headers
        for line in lines[1:]:
            if line == "":  # Skip empty lines (end of headers)
                continue
            if ":" not in line:  # Skip lines without headers (e.g., malformed)
                continue
            header_key, header_value = line.split(":", 1)
            self.headers[header_key.strip()] = header_value.strip()
        
        # Parse body (if present)
        if "Content-Length" in self.headers:
            content_length = int(self.headers["Content-Length"])
            self.body = self.data[-content_length:]  # Extract body from request data
        
    def __repr__(self):
        return f"HttpRequest(method={self.method}, path={self.path}, version={self.version}, headers={self.headers}, body={self.body})"
    
if __name__ == "__main__":
    # Example usage:
    data = """POST /files/number HTTP/1.1\r
    Host: localhost:4221\r
    User-Agent: curl/7.64.1\r
    Accept: */*\r
    Content-Type: application/octet-stream\r
    Content-Length: 5\r
    \r
    12345"""

    request = HttpRequest(data)
    print(request)