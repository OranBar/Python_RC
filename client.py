# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 02:50:57 2017

@author: King Pub
"""
import socket
from protocol import *

class Client(object):

    name = "myname"
    clientSocket = None

    def __init__(self, myName):
        self.name = myName

    def connect(self, serverName, serverPort):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((serverName, serverPort))

    def send_message(self, msg):
        assert (self.clientSocket != None)

        self.clientSocket.send(msg.pack_data())
        #chiedi a dani se esiste recv e basta
        answer, serverAddress = self.clientSocket.recvfrom(2048)
        answer_packet = ProtocolPacket.unpack_data(answer)
        return answer_packet

    def close_connection(self):
        self.clientSocket.close()
        