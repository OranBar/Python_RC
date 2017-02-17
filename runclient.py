# pylint: disable=C0103

from client import Client
from protocol import *

if __name__ == "__main__":
    try:
        client = Client('me')
        client.connect('localhost', 12002)

        packet = ProtocolPacket(Commands.LOGIN, 0, 'pazzi', 'gabbiani')
        answer = client.send_message(packet)
        print answer.arg1 + ' ' + answer.arg2
    finally:
        client.close_connection()


