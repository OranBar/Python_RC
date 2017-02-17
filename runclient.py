# pylint: disable=C0103

from client import Client
from protocol import *

if __name__ == "__main__":
    client = Client('me')
    packet = ProtocolPacket(Commands.LOGIN, 0, 'pazzi', 'gabbiani')
    answer = client.send_message('localhost', 12000, packet, 1)
    print answer.arg1 + answer.arg2

