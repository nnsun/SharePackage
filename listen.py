import socket

port = 9999

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostname(), 9999))
    server_socket.listen(25)
    conn, addr = server_socket.accept()
    print(conn.recv(1000))


if __name__ == "__main__":
    main()
