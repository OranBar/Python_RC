# pylint: disable=C0111

from enum import Enum

class Commands(Enum):
    LOGIN = 0
    REGISTER = 1
    SELL = 2
    OFFER = 3
    NOTIFYME = 4

class ProtocolPacket(object):

    cmd = 0
    authenticated = 0
    arg1 = 0
    arg2 = 0
    opresult = 0

    def __init__(self, cmd, authenticated, arg1, arg2, opresult):
        self.cmd = cmd
        self.authenticated = authenticated
        self.arg1 = arg1
        self.arg2 = arg2
        self.opresult = opresult



