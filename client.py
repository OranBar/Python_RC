# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 02:50:57 2017

@author: King Pub
"""
import socket
from protocol import *
import sys
from threading import Thread


class Client(object):

    clientSocket = None
    notifications_socket = None
    connection_open = False

    #Variable used for testing
    last_recv_notification = ''

    def connect(self, serverName, serverPort):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((serverName, serverPort))
        
        connection_open = True

        self.__connect_to_notification_minion()
        
        notification_listener_thread = Thread(target =  self.__echo_socket_messages, args = ())
        notification_listener_thread.start()
        
        # self.__echo_socket_messages()

    def __connect_to_notification_minion(self):
        answer = self.send_message( ProtocolPacket(Commands.CONNECT, 0, '', '') )
        
        assert answer.opresult == OpResult.SUCCESS
        
        self.notifications_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The socket port is saved into price
        print 'Connecting to '+answer.arg1+' '+int(answer.price).__str__()
        self.notifications_socket.connect( (answer.arg1, int(answer.price)) )

    def __echo_socket_messages(self):
        assert (self.notifications_socket != None)

        while self.connection_open:
            notification_msg = self.notifications_socket.recv(2048)
            last_recv_notification = notification_msg
            print '\033[94m'+ notification_msg
            sys.stdout.flush()
    
    def send_message(self, msg):
        assert (self.clientSocket != None)

        self.clientSocket.send(msg.pack_data())
        answer_packet = self.clientSocket.recv(2048)
        answer = ProtocolPacket.unpack_data(answer_packet)
        return answer

    def close_connection(self):
        assert (self.clientSocket != None)

        connection_open = False

        # Close connection with server
        closeMsg = ProtocolPacket(Commands.CLOSE_CONNECTION, 0, '', '')
        answer = self.send_message( closeMsg )
        if answer.opresult == OpResult.SUCCESS:
            # print "Client: Connection closed"
            self.clientSocket.close()
        else:
            print 'Error closing the connection'

        #Close notification socket
        self.notifications_socket.close()

        

        
        