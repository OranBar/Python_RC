# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 02:50:57 2017

@author: King Pub
"""

import socket

serverName = 'localhost'
serverPort = 12000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = raw_input('Insert\n')
clientSocket.sendto(message, (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage)
clientSocket.close()
print('Finish')