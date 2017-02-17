from server import *

try:
    server = MockServer('localhost', 12000)
    server.start_server()
finally:
    server.stop_server()