from multiconnServer import WebServer
from GetDecorator import GET
 

class Main():
    pass
if __name__ == "__main__":
    server = WebServer(host="127.0.0.1", port=65432)
    #Methods
    @GET("/hello")
    def helloHandler():
        return f"HTTP/1.1 200 OK\r\nContent-Length: {len('hello')}\r\n\r\nhello"
    @GET("/hello/*")
    def helloHandler():
        return f"HTTP/1.1 200 OK\r\nContent-Length: {len('hello/* route')}\r\n\r\nhello/* route"
    @GET("/hello/*/hi")
    def helloHandler():
        return f"HTTP/1.1 200 OK\r\nContent-Length: {len('/hello/*/hi route')}\r\n\r\n/hello/*/hi route"
    server.start_server()
