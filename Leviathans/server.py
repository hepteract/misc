import subprocess
import socket

def main(*args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 1701))
    sock.listen(5)
    while True:
        client, address = sock.accept()
        fd = client.makefile()
        print "Connection from", address[0]
        subprocess.Popen(args, stdin = fd, stdout = fd, stderr = fd)

if __name__ == "__main__":
    main("bash")
