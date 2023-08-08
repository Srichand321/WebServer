class Routes:
    
    
    def __init__(self):
        self.routes = {}
        self.add_routes("/hello", self.hello_page)
    
    def add_routes(self, path, handler):
        self.routes[path] = handler

    def handle_request(self, path):
        if path in self.routes:
            return self.routes[path]()
        else:
            return "HTTP/1.1 400 Bad Request\r\nContent-Length: 11\r\n\r\nBad Request"
        
    def hello_page(self):
        return "HTTP/1.1 200 OK\r\nContent-length:5\r\n\r\nHello"
    
