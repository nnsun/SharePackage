import json
import socket
import sqlite3
import threading


port = 9999

def main():
    connection = sqlite3.connect("tracker.db")
    cursor = connection.cursor()

    with open("schema.sql", 'r') as schema:
        sql_init = schema.read()

    cursor.executescript(sql_init)
    connection.commit()
    connection.close()

    ip = get_ip()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(25)
    try:
        while True:
            conn, addr = server_socket.accept()
            ConnectionThread(conn, addr).start()
    except KeyboardInterrupt:
        server_socket.close()


class ConnectionThread(threading.Thread):
    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr[0]

    def run(self):
        # commands can either be "install <package name>" or "create <manifest>"
        data = self.conn.recv(1024).decode("utf-8").split(' ', 1)
        if data[0] == "install":
            if len(data) != 2:
                self.conn.close()
            self.install(data[1])
        elif data[0] == "create":
            if len(data) != 2:
                self.conn.close()
            self.create(data[1])
        else:
            self.conn.close()


    def install(self, name):
        connection = sqlite3.connect("tracker.db")
        cursor = connection.cursor()
        command = "SELECT pFILES FROM Packages WHERE pName = '" + name + "'"
        cursor.execute(command)
        result = cursor.fetchone()[0]
        self.conn.send(str.encode(result))

        command = "SELECT IP FROM PeersMap WHERE pName = '" + name + "'"
        cursor.execute(command)
        result = cursor.fetchall()

        for row in result:
            self.conn.send(str.encode(row[0] + '\n'))
        self.conn.send(b"END")
        connection.close()


    def create(self, manifest):
        connection = sqlite3.connect("tracker.db")
        cursor = connection.cursor()
        manifest_dict = json.loads(manifest)

        command = "SELECT * FROM Packages WHERE pName = '" + manifest_dict["name"] + "'"
        cursor.execute(command)
        if cursor.rowcount != 0:
            self.conn.close()

        raw_files = manifest_dict["files"]
        files_str = ""
        for file_str in raw_files:
            if files_str:
                files_str += '|'
            files_str += file_str[0] + ' ' + str(file_str[1])

        # TODO: encode dependencies string
        command = ("INSERT INTO Packages VALUES ('" + manifest_dict["name"] + "','" +
                manifest_dict["description"] + "','" + manifest_dict["version"] +
                "','" + manifest_dict["author"] + "','" + "" +
                "','" + files_str + "')")
        cursor.execute(command)

        command = ("INSERT INTO PeersMap VALUES ('" + manifest_dict["name"] + "','" + self.addr + "')")
        cursor.execute(command)

        connection.commit()
        connection.close()
        print("Added package " + manifest_dict["name"] + " to tracker")


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip



if __name__ == "__main__":
    main()