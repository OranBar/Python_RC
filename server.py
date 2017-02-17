# -*- coding: utf-8 -*-
# pylint disable=C0103
# pylint disable=C0303

"""
Created on Thu Feb 16 02:49:37 2017

@author: King Pub
"""
import socket
from enum import Enum
from threading import Thread
from time import sleep
import time

class ConnectionFSM(Enum):
    START = 0
    CONNECTED = 1
    LOGIN = 2
    AUTHENTICATED = 3
    END = 4


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
                # thread = Thread(target = self.process_message, args = (message, clientAddress))
                # thread.start()
                self.process_message(message, clientAddress)
        finally:
            self.serverSocket.close()

    def stop_server(self):
        stop = True

    def process_message(self, msg, clientAddress):
        modifiedMessage = (msg[0].upper(), msg[1].upper())
        self.serverSocket.sendto(modifiedMessage, clientAddress)

# class MessageHandler(object):

#     state = ConnectionFSM.START 

#     def serve_client(self, msg, state):
#         if(state == ConnectionFSM.START):
#         #    Authenticate(msg.arg1, msg.arg2) 
#         elif(state == ConnectionFSM.CONNECTED):
#             pass
#         elif(state == ConnectionFSM.AUTHENTICATED):
#             pass
#         elif(state == ConnectionFSM.END):
#             pass
    


    

