from server import *

if __name__ == "__main__":
    try:
        server = Server('localhost', 12000)
        server.start_server()
    finally:
        server.stop_server()    
