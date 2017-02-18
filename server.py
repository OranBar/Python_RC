# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 02:49:37 2017

@author: King Pub
"""
import socket
from enum import Enum
from threading import Thread
from time import sleep
import time
from protocol import *
from copy import *
from database import *

class ConnectionFSM(Enum):
    LOGIN = 1
    AUTHENTICATED = 2


class Server(object):

    serverName = 'localhost'
    serverPort = 12000
    serverSocket = 0

    stop = 0

    def __init__(self, serverName, serverPort):
        self.serverName = serverName
        self.serverPort = serverPort

        print 'Server Initialized: (Name {0}, Port {1})'.format( self.serverName, self.serverPort)
        
    def start_server(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.serverName, self.serverPort))
        self.serverSocket.listen(5)
        print('Server Listening')
        try:
            while(self.stop == False):
                conn, addr = self.serverSocket.accept()
                print 'New Client Connected'
                self.process_connection(conn)
        finally:
            self.serverSocket.close()

    def process_connection(self, conn):
        msgHandler = ServerMinion()
        print 'Starting Minion Thread'
        serverMinionThread = Thread(target =  msgHandler.serve_client, args = (conn, ConnectionFSM.LOGIN))
        serverMinionThread.start()
        
    def stop_server(self):
        stop = True

class MockServer(Server):

    def process_connection(self, connection):
        packed_msg = connection.recv(2048)
        #Temporal Fix
        if(packed_msg == ''):
            connection.close()
            return
        
        msg = ProtocolPacket.unpack_data(packed_msg)
        msg.arg1 = msg.arg1.upper()
        msg.arg2 = msg.arg2.upper()
        connection.send(msg.pack_data())
        connection.close()

class ServerMinion(object):

    def serve_client(self, connection, state):
        print '\nServe_Client: State is ' + state.__str__()

        #Add timeout
        packed_msg = connection.recv(2048)
        #Temporal Fix
        if(packed_msg == ''):
            connection.close()
            print 'Detected closed socket. Closing Connection'
            return
        
        msg = ProtocolPacket.unpack_data(packed_msg)
        
        print 'Message Received: ' + msg.__str__()
        
        if(state is ConnectionFSM.LOGIN):
            self.__handle_login(connection, msg)
            
        elif(state is ConnectionFSM.AUTHENTICATED):
            self.__handle_request(connection, msg)
      

    def __handle_login(self, connection, msg):
        answer = msg
        
        if(msg.cmd != Commands.LOGIN):
            #Error: bad request: User needs to login before doing any other operation
            print 'Error: Need to login first'
            answer.opresult = OpResult.USER_NOT_AUTHENTICATED
            connection.send( answer.pack_data() )
            self.serve_client(connection, ConnectionFSM.LOGIN)
        else:
            username, password = msg.arg1, msg.arg2
            print 'Username is {0}, password is {1}'.format(username, password)
            database = Database()
            loginResult = database.check_credentials(username, password)
            # loginResult = self.__try_login(username, password)
            print 'Login Successful: ' + loginResult.__str__()
            answer.opresult = loginResult

            connection.send( answer.pack_data() ) 
            
            if loginResult == OpResult.SUCCESS:
                self.serve_client(connection, ConnectionFSM.AUTHENTICATED)
            else:
                self.serve_client(connection, ConnectionFSM.LOGIN)
        

    # def __try_login(self, username, password):
    #     #TODO dummy implementation
    #     if user != 'user'
    #         return OpResult.INVALID_USERNAME
    #     elif password != 'password'
    #         return OpResult.INVALID_PASSWORD
    #     else:
    #         return OpResult.SUCCESS

    def __handle_request(self, connection, msg):
        #TODO Implement me
        pass



    

