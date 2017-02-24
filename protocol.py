from enum import *
import struct
import socket
import collections

Product = collections.namedtuple('Product', 'name category')

@unique
class Commands(IntEnum):
    LOGIN = 0
    REGISTER = 1
    SELL = 2
    OFFER = 3
    NOTIFYME_PRODUCT_CHANGE = 4
    NOTIFYME_NEW_PRODUCTS = 5
    NOTIFYME_ALL = 6
    CLOSE_CONNECTION = 7

class NotificationType(IntEnum):
    HIGHER_BID = 0
    NEW_PRODUCT = 1
    PRODUCT_SOLD = 2

    

@unique
class OpResult(IntEnum):
    ### Generic Results ##
    NONE = 0
    SUCCESS = 1
    TIMEOUT = 2
    # Database Results # 
    ### Registration Results ###
    USER_ALREADY_EXISTS = 3
    ### Login Results ##
    INVALID_USERNAME = 4
    INVALID_PASSWORD = 5
    USER_NOT_FOUND = 6
    INCORRECT_PASSWORD = 7
    USER_NOT_AUTHENTICATED = 8
    ALREADY_AUTHENTICATED = 9
    ### Product Results ##
    INVALID_PRODUCT_NAME = 10
    INVALID_CATEGORY_NAME = 11
    PRODUCT_ALREADY_EXISTS = 12
    CATEGORY_ALREADY_EXISTS = 13
    CATEGORY_NOT_FOUND = 14
    PRODUCT_NOT_FOUND = 15
    BID_TOO_LOW = 16


class ProtocolPacket(object):

    cmd = 0
    opresult = 0
    arg1 = 0
    arg2 = 0
    price = 0

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
        return '({0}, {1}, {2}, {3}, {4})'.format(Commands(self.cmd).__str__(), OpResult(self.opresult).__str__(), self.arg1, self.arg2, self.price)

   