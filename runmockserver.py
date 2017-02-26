from server import *

if __name__ == "__main__":
    server = MockServer('localhost', 49152)
    server.start_server()
