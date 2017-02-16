# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 02:49:37 2017

@author: King Pub
"""

import socket

serverName = 'localhost'
serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('Server Ready')
try:
    while(1):
        message, clientAddress = serverSocket.recvfrom(2048)    
        modifiedMessage = message.upper()
        serverSocket.sendto(modifiedMessage, clientAddress)
finally:
    serverSocket.close()