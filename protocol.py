# pylint: disable=C0111

from enum import IntEnum
import struct
import socket

@unique
class Commands(IntEnum):
    LOGIN = 0
    REGISTER = 1
    SELL = 2
    OFFER = 3
    NOTIFYME = 4
    
@unique
class OpResult(IntEnum):
    ### Generic Results ##
    NONE = 0
    SUCCESS = 1
    TIMEOUT = 2
    ## Database Results ## 
    ### Login Results ##
    INVALID_USERNAME = 3
    INVALID_PASSWORD = 4
    USER_NOT_AUTHENTICATED = 5
    ALREADY_AUTHENTICATED = 6
    ### Product Results ##
    INVALID_PRODUCT_NAME = 7
    INVALID_CATEGORY_NAME = 8
    PRODUCT_ALREADY_EXISTS = 9
    CATEGORY_ALREADY_EXISTS = 10
    CATEGORY_NOT_FOUND = 11
    PRODUCT_NOT_FOUND = 11
    


class ProtocolPacket(object):

    cmd = 0
    opresult = 0
    arg1 = 0
    arg2 = 0
    price = 0

    ## Price is only used for Offers. 
    def __init__(self, cmd, opresult, arg1, arg2, price=0):
        self.cmd = cmd
        self.opresult = opresult
        self.arg1 = arg1
        self.arg2 = arg2
        self.price = price

    def pack_data(self):
        arg1b = bytes(self.arg1)
        arg2b = bytes(self.arg2)
        values = (len(arg1b), len(arg2b), self.cmd, self.opresult, arg1b, arg2b, self.price)
        packed_data = struct.pack('I I I I {0}s {1}s f'.format(len(arg1b), len(arg2b)), *values)
        return packed_data

    @staticmethod
    def unpack_data(packedData):
        (arg1Size, arg2Size), data = struct.unpack('I I', packedData[:8]), packedData[8:]
        unpacker = struct.Struct( ('I I {0}s {1}s f').format(arg1Size, arg2Size) )
        unpacked_data = unpacker.unpack(data)
        return ProtocolPacket(*unpacked_data) 

    def __str__(self):
        return '({0}, {1}, {2}, {3}, {4})'.format(self.cmd, self.opresult, self.arg1, self.arg2, self.price)

   