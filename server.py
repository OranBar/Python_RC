"""
Created on Thu Feb 16 02:49:37 2017

@author: King Pub
"""
import socket
import copy
from enum import Enum
from threading import Thread
from time import sleep
import time
from protocol import *

class ConnectionFSM(Enum):
    LOGIN = 0
    AUTHENTICATED = 1


class Server(object):

    serverName = 'localhost'
    serverPort = 12000
    serverSocket = 0

    stop = 0

    def __init__(self, serverName, serverPort):
        self.serverName = serverName
        self.serverPort = serverPort
        
    def start_server(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(('', self.serverPort))
        self.serverSocket.listen(10)
        print('Server Ready')
        try:
            while(self.stop == False):
                conn, addr = self.serverSocket.accept()
                serverMinionThread = Thread(target =  self.__process_connection, args = (conn,))
                serverMinionThread.start()
                # self.process_message(unpacked_msg, conn)
        finally:
            self.serverSocket.close()

    def __process_connection(self, connection):
        msgHandler = ServerMinion()
        msgHandler.serve_client(connection)

    def stop_server(self):
        stop = True

    
class MockServer(Server):

    def __process_message(self, msg, connection):
        
        msg.arg1 = msg.arg1.upper()
        msg.arg2 = msg.arg2.upper()
        
        connection.send(msg.pack_data())

class ServerMinion(object):

    def serve_client(self, connection, state = ConnectionFSM.LOGIN):
        #Add timeout
        packed_msg = connection.recv(2048)
        msg = ProtocolPacket.unpack_data(packed_msg)
        
        if(state is ConnectionFSM.LOGIN):
            self.__handle_login(connection, msg)
            
        elif(state is ConnectionFSM.AUTHENTICATED):
            self.__handle_request(connection, msg)


    def __handle_login(self, connection, msg):
        answer = copy.copy(msg)
        
        if(msg.cmd is not Commands.LOGIN):
            #Error: bad request: User needs to login before doing any other operation
            answer.opresult = OpResult.USER_NOT_AUTHENTICATED
            connection.send( answer.pack_data() )
            self.serve_client(connection, ConnectionFSM.LOGIN)
        
        username, password = msg.arg1, msg.arg2
        answer.opresult = __try_login(username, password)

        connection.send(answer) 
        
        if answer.opresult is LoginResults.SUCCESS:
            self.serve_client(connection, ConnectionFSM.AUTHENTICATED)
        else:
            self.serve_client(connection, ConnectionFSM.LOGIN)
        

    def __try_login(self, username, password):
        #TODO implement me
        return LoginResults.SUCCESS 

    def __handle_request(self, connection, msg):
        #TODO Implement me
        pass



    

