# pylint: disable=C0103

from server import *

if __name__ == "__main__":
    server = Server('localhost', 12000)
    server.start_server()

