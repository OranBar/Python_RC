from server import *

if __name__ == "__main__":
    server = MockServer('localhost', 12000)
    server.start_server()
