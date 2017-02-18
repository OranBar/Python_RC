# pylint: disable=C0111

from enum import IntEnum
import struct
import socket

class Commands(IntEnum):
    LOGIN = 0
    REGISTER = 1
    SELL = 2
    OFFER = 3
    NOTIFYME = 4

class OpResult(IntEnum):
    ### Generic Results ##
    NONE = 0
    SUCCESS = 1
    TIMEOUT = 2
    ### Login Results ##
    INVALID_USERNAME = 3
    INVALID_PASSWORD = 4
    USER_NOT_AUTHENTICATED = 5

class ProtocolPacket(object):

    cmd = 0
    opresult = 0
    arg1 = 0
    arg2 = 0

    def __init__(self, cmd, opresult, arg1, arg2):
        self.cmd = cmd
        self.opresult = opresult
        self.arg1 = arg1
        self.arg2 = arg2

    def send_on_socket(self, socket):
        socket.send( pack_data() )
       
    def pack_data(self):
        arg1b = bytes(self.arg1)
        arg2b = bytes(self.arg2)
        values = (len(arg1b), len(arg2b), self.cmd, self.opresult, arg1b, arg2b)
        packed_data = struct.pack('I I I I {0}s {1}s'.format(len(arg1b), len(arg2b)), *values)
        return packed_data

    @staticmethod
    def unpack_data(packedData):
        (arg1Size, arg2Size), data = struct.unpack('I I', packedData[:8]), packedData[8:]
        unpacker = struct.Struct( ('I I {0}s {1}s').format(arg1Size, arg2Size) )
        unpacked_data = unpacker.unpack(data)
        return ProtocolPacket(*unpacked_data) 

    def __str__(self):
        return '({0}, {1}, {2}, {3})'.format(self.cmd, self.opresult, self.arg1, self.arg2)


    def __str__(self):
        return '({0}, {1}, {2}, {3})'.format(self.cmd, self.opresult, self.arg1, self.arg2)

   