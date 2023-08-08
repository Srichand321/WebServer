import socket
import selectors
import types
from GetDecorator import GET
from HttpRequest import HttpRequest


class WebServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sel = selectors.DefaultSelector()

        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((self.host, self.port))
        lsock.listen()

        print(f"Listening on {self.host}:{self.port}")
        lsock.setblocking(False)

        self.sel.register(lsock, selectors.EVENT_READ, data=None)

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events=events, data=data)

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            # print(recv_data)
            if recv_data:
                data.inb += recv_data

            else:
                print(f"Closing connection to {data.addr}")
                self.sel.unregister(sock)
                sock.close()

        if mask & selectors.EVENT_WRITE:
            if data.inb:
                request = HttpRequest(data.inb)
                data.outb = request.handleRequest()
                data.outb = data.outb.encode('utf-8')
                #print(data.outb)

                print(f"Echoing response to {data.addr}")
                try:
                    sent = sock.send(data.outb)  # Should be ready to write
                except (ConnectionAbortedError, OSError) as e:
                    print(f"Connection error with {data.addr}: {e}")
                    self.sel.unregister(sock)
                    sock.close()

                # Clear the data buffer after sending the response
                data.inb = b""
                data.outb = b""

    def start_server(self):
        try:
            while True:
                events = self.sel.select()
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)

        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")

        finally:
            self.sel.close()
