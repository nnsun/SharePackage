import socket

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
    server_socket.bind((ip, 9999))
    server_socket.listen(25)
    conn, addr = server_socket.accept()
    print(conn.recv(1000))


if __name__ == "__main__":
    main()
