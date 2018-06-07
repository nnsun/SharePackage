import json
import os
import socket
import sys
import threading


port_num = 9999
tracker_ip = "192.241.128.177"

def main(args):
    if len(args) < 2 or len(args) > 3:
        error("Usage: python client.py args")

    arg1 = args[1]

    # set up user local files if needed
    home = os.path.expanduser("~")
    # dot_dir = home + "/.p2p-pm"
    # if not os.path.isdir(dot_dir):
    #     os.mkdir(dot_dir)

    # index = dot_dir + "/index"
    # if not os.path.isfile(index):
    #     open(index, 'w').close()

    pm_dir = home + "/p2p-pm"
    if not os.path.isdir(pm_dir):
        os.mkdir(pm_dir)

    package_dir = home + "/p2p-pm/packages"
    if not os.path.isdir(package_dir):
        os.mkdir(package_dir)

    if arg1 == "version":
        print("p2p-pm 0.1.0")
    elif arg1 == "install":
        if len(args) != 3:
            error("Usage: python client.py install <package name>")
        install(args[2])
    elif arg1 == "create":
        if len(args) != 3:
            error("Usage: python client.py create <package path>")
        create(args[2])
    elif arg1 == "help":
        print_help()
    else:
        error("Usage: python client.py args")


def print_help():
    print("Usage: python client.py <install/create/version/help> args")
    print("Command  Args")
    print("install  <package name>")
    print("create   <package path>")
    print("version")
    print("help")


def error(msg):
    print(msg)
    exit(1)


def install(package):
    sock = connect_tracker()

    sock.send(str.encode("install " + package))

    files = sock.recv(4096)

    peers = []
    peer = sock.recv(4096)
    while peer:
        peers.append(peer)
        peer = sock.recv(4096)

    assignment = assign_files(peers, files)
    for peer in assignment:
        files = assignment[peer]
        ReceiveThread(peer, files).start()


def connect_tracker():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((tracker_ip, port_num))
    return sock


def validate_json(j):
    json_dict = json.loads(j)
    try:
        if (type(json_dict["name"]) != str or type(json_dict["description"]) != str
                or type(json_dict["version"]) != str or type(json_dict["author"]) != str
                or type(json_dict["dependencies"]) != list):
            error("Error: manifest file is corrupted")
    except KeyError:
        error("Error: manifest file is corrupted")
    return json_dict


def create(path):
    if not os.path.isdir(path):
        error("Package directory not found")

    if not os.path.isfile(path + "/manifest.json"):
        error("Manifest file not found")

    if not os.path.isfile(path + "/install.sh"):
        error("Install script not found")

    with open(path + "/manifest.json", 'r') as manifest:
        json_str = manifest.read()

    json_dict = validate_json(json_str)

    files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            if file_path != path + "/manifest.json":
                files.append([file_path, os.path.getsize(file_path)])

    json_dict["files"] = files
    manifest_json = json.dumps(json_dict)
    with open(path + "/manifest.json", 'w') as manifest:
        manifest.write(manifest_json)

    sock = connect_tracker()
    sock.send(str.encode(manifest_json))


def assign_files(peers, files):
    sorted_files = sorted(files, key=lambda x: x[1])

    file_assignment = dict.fromkeys(peers, [])

    for i in range(len(files)):
        peer = peers[i % len(peers)]
        file_assignment[peer] = file_assignment[peer].append(sorted_files[i])

    return file_assignment


class ReceiveThread(threading.Thread):
    def __init__(self, addr, files):
        super().__init__()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(addr, 9999)
        self.files = files

    def run(self):
        files_str = ""
        for file in self.files:
            if files_str:
                files_str += ','
            files_str += file
        self.client_socket.send(str.encode(files_str))

        for file in self.files:
            with open(file, 'wb') as f:
                data = self.conn.recv(4096)
                while data:
                    f.write(data)
                    data = self.conn.recv(4096)


if __name__ == "__main__":
    main(sys.argv)
