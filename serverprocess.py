# pylint: disable=C0103

from server import *

server = Server('localhost', 12000)
server.start_server()

