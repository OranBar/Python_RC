# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 02:50:57 2017

@author: King Pub
"""
import socket

class Client(object):

    name = "myname"

    def __init__(self, myName):
        self.name = myName

    def send_message(self, serverName, serverPort,  msg, answerExpected):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientSocket.send(msg)
        if answerExpected:
            answer, serverAddress = clientSocket.recvfrom(2048)
            return answer
        else: 
            return 0
