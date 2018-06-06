import json
import os
import socket
import sys


port_num = 8765

def main(args):
    if len(args) < 2 or len(args) > 3:
        error("Usage: python client.py args")

    arg1 = args[1]

    # set up uesr local files if needed
    home = os.path.expanduser("~")
    dot_dir = home + "/.p2p-pm"
    if not os.path.isdir(dot_dir):
        os.mkdir(dot_dir)

    index = dot_dir + "/index"
    if not os.path.isfile(index):
        open(index, 'w').close()


    package_dir = home + "/p2p-pm"
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
            error("Usage: python client.py create <package path")
        create(args[2])
    elif arg1 == "help":
        print_help()
    else:
        error("Usage: python client.py args")

def print_help():
    print("Usage: python client.py <install/create/version/help> args")
    # TODO: fill in rest

def error(msg):
    print(msg)
    exit(1)


def install(package):
    pass

def connect_tracker():
    pass

def validate_json(j):
    json_dict = json.loads(j)
    try:
        # TODO: fill in
        pass
    except KeyError:
        error("Error: manifest file is corrupted")

    return json_dict

def create(path):
    if not os.path.isdir(path):
        error("...")
    if not os.path.isfile(path + "/manifest.json"):
        error("..")
    if not os.path.isfile(path + "/install.sh"):
        error("")

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


def connect_peer(ip):
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


if __name__ == "__main__":
    main(sys.argv)
