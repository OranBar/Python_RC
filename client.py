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
        answer_packet = self.clientSocket.recv(2048)
        answer = ProtocolPacket.unpack_data(answer_packet)
        return answer

    def close_connection(self):
        assert (self.clientSocket != None)

        closeMsg = ProtocolPacket(Commands.CLOSE_CONNECTION, 0, '', '')
        answer = self.send_message(closeMsg)
        if answer.opresult == OpResult.SUCCESS:
            self.clientSocket.close()
        else:
            print 'Error closing the connection'
        