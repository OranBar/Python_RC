# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 02:50:57 2017

@author: King Pub
"""
import socket
from protocol import *

class Client(object):

    name = "myname"

    def __init__(self, myName):
        self.name = myName

    def send_message(self, serverName, serverPort,  msg):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientSocket.send(msg)
        #chiedi a dani se esiste recv e basta
        answer, serverAddress = clientSocket.recvfrom(2048)
        answer_packet = ProtocolPacket.unpack_data(answer)
        return answer_packet
        