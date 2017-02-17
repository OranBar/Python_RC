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
                serverMinionThread = Thread(target =  self.__process_message, args = (unpacked_msg, conn))
                serverMinionThread.start()
                # self.process_message(unpacked_msg, conn)
        finally:
            self.serverSocket.close()

    def stop_server(self):
        stop = True

    def __process_message(self, msg, connection):
        msgHandler = ServerMinion()
        msgHandle.serve_client(conn)

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
        answer = msg.copy()

        if(state is ConnectionFSM.LOGIN):
            handle_login(msg)
            
        elif(state is ConnectionFSM.AUTHENTICATED):
            self.__handle_request(msg)


    def __handle_login(connection, msg):
        if(msg.cmd is not Commands.LOGIN):
            #Error: bad request: User needs to login before doing any other operation
            answer.opresult = LoginResults.USER_NOT_AUTHENTICATED
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

    def __handle_request(self, msg):
        #TODO Implement me
        pass



    

