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
import sys
import itertools

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
        self.database = DatabaseAPI()

        print 'Server Initialized: (Name {0}, Port {1})'.format( self.serverName, self.serverPort)
        
    def start_server(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.serverName, self.serverPort))
        self.serverSocket.listen(5)
        print('Server Listening')
        try:
            while(True):
                conn, addr = self.serverSocket.accept()
                print 'New Client Connected'
                self.process_connection(conn)
        finally:
            self.serverSocket.close()

    def process_connection(self, conn):
        msgHandler = ServerMinion()
        print 'Starting Minion Thread'
        serverMinionThread = Thread(target =  msgHandler.connect_to_minion, args = (self.database, conn, ConnectionFSM.LOGIN, ''))
        serverMinionThread.start()
    

class MockServer(Server):

    def __init__(self, serverName, serverPort):
        Server.__init__(self, serverName, serverPort)
        self.database.register_new_user('user', 'pass')       
        self.database.register_new_user('user2', 'pass')
        self.database.register_new_user('user3', 'pass')

class ServerMinion(object):
    #Static shared variable 
    next_available_port = 49152

    notificationDaemon = None

    def connect_to_minion(self, database, connection, state, client_username):
        print '\nServe_Client: State is ' + state.__str__()
        
        packed_msg = connection.recv(2048)
        msg = ProtocolPacket.unpack_data(packed_msg)
        assert msg.cmd == Commands.CONNECT

        notificationDaemonPort = ServerMinion.next_available_port
        ServerMinion.next_available_port += 1
        self.notificationDaemon = NotificationDaemon(notificationDaemonPort)
        
        notificationDaemon_thread = Thread(target =  self.notificationDaemon.start, args = (database, notificationDaemonPort))
        notificationDaemon_thread.start()
        
        msg.arg1 = self.notificationDaemon.name
        # Although semantically wrong, it is better to save the port number as a variable that 
        # represents an numeric value, such as price
        msg.price = self.notificationDaemon.port
        msg.opresult = OpResult.SUCCESS
        connection.send ( msg.pack_data() )

        self.serve_client(database, connection, state, client_username)
    
    def serve_client(self, database, connection, state, client_username):
        # print '\nServe_Client: State is ' + state.__str__()
        
        # packed_msg = connection.recv(2048)
        # assert packed_msg.cmd == Commands.CONNECT

        
        # notificationDaemonPort = ServerMinion.next_available_port
        # ServerMinion.next_available_port += 1
        # self.notificationDaemon = NotificationDaemon()
        
        # notificationDaemon_thread = Thread(target =  self.notificationDaemon.start, args = (database, notificationDaemonPort))
        # notificationDaemon_thread.start()
        
        # msg.arg1 = self.notificationDaemon.name
        # msg.arg2 = self.notificationDaemon.port
        # msg.opresult = OpResult.SUCCESS
        # connection.send ( msg.pack_data() )
        
        #Add timeout
        packed_msg = connection.recv(2048)
        
        if(packed_msg == ''):
            connection.close()
            print 'WARNING: Detected closed socket. Please close the connection using the Close_Connection command'
            return
        
        msg = ProtocolPacket.unpack_data(packed_msg)
        
        sys.stdout.flush()
        print 'Message Received: ' + msg.__str__()
        
        self.__handle_request(database, connection, msg, state, client_username)

     
    def __handle_request(self, database, connection, msg, state, client_username):
        #TODO Implement me
        cmd = msg.cmd

        if( cmd == Commands.CLOSE_CONNECTION):
            msg.opresult = OpResult.SUCCESS
            connection.send( msg.pack_data() )
            print 'Server: Closing Connection'
            connection.close()
            return

        # if(cmd == Commands.CONNECT):
        #     # Send NotificationDaemon name and port
        #     msg.arg1 = self.notificationDaemon.name
        #     msg.arg2 = self.notificationDaemon.port
        #     msg.opresult = OpResult.SUCCESS
        #     connection.send ( msg.pack_data() )
        #     self.serve_client(database, connection, state, client_username)
        #     return

        if(state is ConnectionFSM.LOGIN):
            self.__handle_login(database, connection, msg)
            return

        if(state is ConnectionFSM.AUTHENTICATED):
            if(cmd == Commands.LOGIN):
                msg.opresult = OpResult.ALREADY_AUTHENTICATED
                
            elif(cmd == Commands.REGISTER):
                msg.opresult = database.register_new_category(msg.arg2)
                
            elif(cmd == Commands.ADD):
                msg.opresult = database.add_product(Product(msg.arg1, msg.arg2), msg.price)
                
            elif(cmd == Commands.OFFER):
                msg.opresult = database.make_offer(Product(msg.arg1, msg.arg2), msg.price, client_username)
    
            elif(cmd == Commands.SELL):
                msg.opresult, msg.price = database.sell_product(Product(msg.arg1, msg.arg2))

            elif(cmd == Commands.NOTIFYME):
                # Check valid Product
                if not database.is_valid_product(product.name):
                    msg.opresult = database.is_valid_product(Product.name)
                else:                    
                    msg.opresult = OpResult.SUCCESS
                
            print 'Result: ' + OpResult(msg.opresult).__str__()
            connection.send ( msg.pack_data() )
            self.serve_client(database, connection, state, client_username)
               


    def __handle_login(self, database, connection, msg):
        answer = msg
        
        if(msg.cmd != Commands.LOGIN):
            #Error: bad request: User needs to login before doing any other operation
            print 'Error: Need to login first'
            answer.opresult = OpResult.USER_NOT_AUTHENTICATED
            print 'Login Result: ' + OpResult.USER_NOT_AUTHENTICATED.__str__()
            connection.send( answer.pack_data() )
            self.serve_client(database, connection, ConnectionFSM.LOGIN, '')
        else:
            username, password = msg.arg1, msg.arg2
            print 'Username is {0}, password is {1}'.format(username, password)
            loginResult = database.check_credentials(username, password)
            print 'Login Result: ' + OpResult(loginResult).__str__()
            answer.opresult = loginResult

            connection.send( answer.pack_data() ) 
            
            if loginResult == OpResult.SUCCESS:
                print 'Login successful. Authenticated as '+username
                self.serve_client(database, connection, ConnectionFSM.AUTHENTICATED, username)
            else:
                self.serve_client(database, connection, ConnectionFSM.LOGIN, '')
        


class NotificationDaemon(object):

    name = ''
    port = 0
    database = None
    connection = None

    products_on_watch = []
    notify_new_products = False
    notify_all = False

    def __init__(self, port):
        self.name = 'localhost'
        self.port = port

    def start(self, database, port):
        # self.name = 'NotificationDaemon'+port.__str__()
        # self.port = port
        print 'NotificationDaemon: Name = {0}, Port = {1}'.format(self.name, self.port)
        self.database = database
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_socket.bind( (self.name, self.port) )
        new_socket.listen(1)
        print 'NotificationDaemon: Listening'
        self.connection, addr = new_socket.accept()
        self.connection.send('Client connection detected')
        print 'NotificationDaemon: Client connection detected'
        

    def register_notification(self, notificationCommand, product):
        assert notificationCommand == Commands.NOTIFYME or notificationCommand == Commands.NOTIFYME_ALL

        if notificationCommand == Commands.NOTIFYME_PRODUCT_CHANGE:
            self.products_on_watch.append(product)
        
        if notificationCommand == Commands.NOTIFYME_NEW_PRODUCTS:
            self.notify_new_products = True

        if notificationCommand == Commands.NOTIFYME_ALL:
            self.notify_all = True

        
    def server_data_changed(self, notificationType, product, price, user):
        if self.connection == None:    
            return
            
        if notificationType == NotificationType.NEW_PRODUCT:
            if notify_new_products or self.notify_all:
                self.send_message('NEW PRODUCT: '+product+' - Start Price: '+price+'Seller: '+user)

        if notificationType == NotificationType.PRODUCT_SOLD:
            if (product in self.products_on_watch) or self.notify_all:
                self.send_message('PRODUCT SOLD: '+product+' - Final Price: '+price+'Sold To: '+user)

        if notificationType == NotificationType.HIGHER_BID:
            if (product in self.products_on_watch) or self.notify_all:
                self.send_message('HIGHER BID: Product: '+product+' - Bid: '+price+'Bidder: '+user)
            
                
        

    def send_message(self, msg):
        self.connection.send('NOTIFICATION MINION: '+msg)
        
