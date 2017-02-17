from server import *

try:
    server = MockServer('localhost', 12002)
    server.start_server()
finally:
    server.stop_server()