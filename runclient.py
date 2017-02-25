# pylint: disable=C0103

from client import Client
from protocol import *

if __name__ == "__main__":
    client = Client()
    client.connect('localhost', 12000)
    
    packet = ProtocolPacket(Commands.LOGIN, 0, 'pazzi', 'gabbiani')
    answer = client.send_message(packet)
    print answer.arg1 + ' ' + answer.arg2
    
    client.close_connection()


