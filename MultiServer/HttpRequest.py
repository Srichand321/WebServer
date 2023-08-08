from GetHandler import GetHandler

class HttpRequest:
    def __init__(self, data):
        self.data = data
        self.method, self.path, self.headers = self.parseRequest(data)

    def parseRequest(self, data):
        request_lines = data.decode("utf-8").split("\r\n")
        method, path, *_ = request_lines[0].split(" ")
        headers = {}
        for i in request_lines[1:]:
            if i:
                key, value = i.split(":",1)
                headers[key] = value
        return method, path, headers
    
    def handleRequest(self):
        if(self.method == "GET"):
            getHandler = GetHandler()
            return getHandler.handleRequest(self.path)
        else:
            return "HTTP/1.1 400 Bad Request\r\nContent-Length: 11\r\n\r\nBad Request"