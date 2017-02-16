# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 02:49:37 2017

@author: King Pub
"""
import socket

class Server(object):

    serverName = 'localhost'
    serverPort = 12000
    serverSocket = 0

    stop = 0

    def __init__(self, serverName, serverPort):
        self.serverName = serverName
        self.serverPort = serverPort
        
    def start_server(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket.bind(('', self.serverPort))
        print('Server Ready')
        try:
            while(self.stop == False):
                message, clientAddress = self.serverSocket.recvfrom(2048)    
                self.process_message(message, clientAddress)
        finally:
            self.serverSocket.close()

    def process_message(self, msg, clientAddress):
        modifiedMessage = msg.upper()
        self.serverSocket.sendto(modifiedMessage, clientAddress)

    def stop_server(self):
        stop = True


# serverName = 'localhost'
# serverPort = 12000
# serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# serverSocket.bind(('', serverPort))
# print('Server Ready')
# try:
#     while(1):
#         message, clientAddress = serverSocket.recvfrom(2048)    
#         modifiedMessage = message.upper()
#         serverSocket.sendto(modifiedMessage, clientAddress)
# finally:
#     serverSocket.close()