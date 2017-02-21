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

    database = None

    def __init__(self, serverName, serverPort):
        self.serverName = serverName
        self.serverPort = serverPort
        self.database = Database()

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
        serverMinionThread = Thread(target =  msgHandler.serve_client, args = (self.database, conn, ConnectionFSM.LOGIN))
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

    def serve_client(self, database, connection, state):
        print '\nServe_Client: State is ' + state.__str__()

        #Add timeout
        packed_msg = connection.recv(2048)
        
        if(packed_msg == ''):
            connection.close()
            print 'WARNING: Detected closed socket. Please close the connection using the Close_Connection command'
            return
        
        msg = ProtocolPacket.unpack_data(packed_msg)
        
        print 'Message Received: ' + msg.__str__()
        
        self.__handle_request(database, connection, msg, state)

        # if(state is ConnectionFSM.LOGIN):
        #     self.__handle_login(connection, msg)
            
        # elif(state is ConnectionFSM.AUTHENTICATED):
        #     self.__handle_request(connection, msg, state)
      

    def __handle_request(self, database, connection, msg, state):
        #TODO Implement me
        cmd = msg.cmd

        if( cmd == Commands.CLOSE_CONNECTION):
            msg.opresult = OpResult.SUCCESS
            connection.send( msg.pack_data() )
            print 'Server: Closing Connection'
            connection.close()
            return

        if(state is ConnectionFSM.LOGIN):
            self.__handle_login(database, connection, msg)

        if(state is ConnectionFSM.AUTHENTICATED):
            if(cmd == Commands.LOGIN):
                msg.opresult = OpResult.ALREADY_AUTHENTICATED
                connection.send( msg.pack_data() )

            elif(cmd == Commands.REGISTER):
                msg.opresult = database.register_new_category(msg.arg2)
                connection.send ( msg.pack_data() )

            elif(cmd == Commands.SELL):
                msg.opresult = database.add_product((msg.arg1, msg.arg2))
                connection.send ( msg.pack_data() )

            elif(cmd == Commands.OFFER):
                pass

            elif(cmd == Commands.NOTIFYME):
                pass        


    def __handle_login(self, database, connection, msg):
        answer = msg
        
        if(msg.cmd != Commands.LOGIN):
            #Error: bad request: User needs to login before doing any other operation
            print 'Error: Need to login first'
            answer.opresult = OpResult.USER_NOT_AUTHENTICATED
            connection.send( answer.pack_data() )
            self.serve_client(database, connection, ConnectionFSM.LOGIN)
        else:
            username, password = msg.arg1, msg.arg2
            print 'Username is {0}, password is {1}'.format(username, password)
            loginResult = database.check_credentials(username, password)
            # loginResult = self.__try_login(username, password)
            print 'Login Successful: ' + loginResult.__str__()
            answer.opresult = loginResult

            connection.send( answer.pack_data() ) 
            
            if loginResult == OpResult.SUCCESS:
                self.serve_client(database, connection, ConnectionFSM.AUTHENTICATED)
            else:
                self.serve_client(database, connection, ConnectionFSM.LOGIN)
        