#www.geeksforgeeks.org/creating-a-proxy-webserver-in-python-set-1/
import socket
import signal

def __init__(self, config):
    signal.signal(signal.SIGINT, self.shutdown)

    self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

