'''
import socket
import selectors
import types
import threading


class WebServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sel = selectors.DefaultSelector()
        self.lock = threading.Lock()

        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((self.host, self.port))
        lsock.listen()

        print(f"Listening on {self.host}:{self.port}")
        #lsock.setblocking(False)

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
            recv_data = sock.recv(1024)
            if recv_data:
                data.inb += recv_data
            else:
                print(f"Closing connection to {data.addr}")
                self.sel.unregister(sock)
                sock.close()

        if mask & selectors.EVENT_WRITE:
            if data.inb:
                response = (
                    "HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\nHello"
                )
                data.outb = response.encode('utf-8')

                print(f"Sending response to {data.addr}")
                try:
                    sent = sock.send(data.outb)
                except (ConnectionAbortedError, OSError) as e:
                    print(f"Connection error with {data.addr}: {e}")
                    self.sel.unregister(sock)
                    sock.close()

                data.inb = b""
                data.outb = b""

    def run_server(self):
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

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 6969
    no_threads = 4  # Number of threads

    server = WebServer(HOST, PORT)
    threads = []

    for _ in range(no_threads):
        thread = threading.Thread(target=server.run_server)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
'''
import socket
import selectors
import types
import multiprocessing

class WebServer:
    def __init__(self, server_socket):
        self.server_socket = server_socket
        self.sel = selectors.DefaultSelector()

        self.sel.register(self.server_socket, selectors.EVENT_READ, data=None)

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
            recv_data = sock.recv(1024)
            if recv_data:
                data.inb += recv_data
            else:
                print(f"Closing connection to {data.addr}")
                self.sel.unregister(sock)
                sock.close()

        if mask & selectors.EVENT_WRITE:
            if data.inb:
                response = (
                    "HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\nHello"
                )
                data.outb = response.encode('utf-8')

                print(f"Sending response to {data.addr}")
                try:
                    sent = sock.send(data.outb)
                except (ConnectionAbortedError, OSError) as e:
                    print(f"Connection error with {data.addr}: {e}")
                    self.sel.unregister(sock)
                    sock.close()

                data.inb = b""
                data.outb = b""

    def run_server(self):
        try:
            while True:
                events = self.sel.select()
                for key, mask in events:
                    if key.fileobj == self.server_socket:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)

        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")

        finally:
            self.sel.close()
            self.server_socket.close()

def run_server_process(server_socket):
    server = WebServer(server_socket=server_socket)
    server.run_server()

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 6969
    no_processes = 4  # Number of processes

    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((HOST, PORT))
    lsock.listen()
    print(f"Listening on {HOST}:{PORT}")
    processes = []

    for _ in range(no_processes):
        process = multiprocessing.Process(target=run_server_process, args=(lsock,))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    lsock.close()  # Close the server socket after all processes have finished
