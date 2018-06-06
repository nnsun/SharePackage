import socket
import threading

port = 9999

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def main():
    ip = get_ip()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(25)
    while True:
        conn, addr = server_socket.accept()
        files = conn.recv(4096).decode("utf-8").split(',')
        ConnectionThread(conn, addr, files).start()


class ConnectionThread(threading.Thread):
    def __init__(self, conn, addr, files):
        super().__init__()
        self.client_socket = conn
        self.files = files
        self.addr = addr

    def run(self):
        for file in self.files:
            with open(file, 'rb') as f:
                buffer = f.read()
                self.client_socket.send(buffer)


if __name__ == "__main__":
    main()
