from protocol import *
from client import *
from server import *
from threading import Thread
import subprocess
import unittest
import time

class DatabaseAPITests(unittest.TestCase):
    def test_register_new_user(self):
        db = DatabaseAPI()

        for user in db.userToPass:
            print user

        self.assertEqual (db.register_new_user('user', 'pass'), OpResult.SUCCESS)
        self.assertEqual (db.register_new_user('user', 'pass'), OpResult.USER_ALREADY_EXISTS)

    def test_product_exists(self):
        db = DatabaseAPI()
        product1 = Product('apple', 'pen')
        db.register_new_category('pen')
        db.add_product(product1, 10.00, 'user')

        self.assertEqual (db.product_exists(Product('apple', 'pen')), OpResult.SUCCESS)
       
        self.assertEqual (db.product_exists( Product('apple', 'yaw') ), OpResult.PRODUCT_NOT_FOUND)

    def test_find_products(self):
        db = DatabaseAPI()
        product1 = Product('cat', 'animal')
        product2 = Product('cat', 'petanimals')
        db.register_new_category('animal')
        db.register_new_category('petanimals')
        db.add_product(product1, 10.00, 'user')
        db.add_product(product2, 15.00, 'user')

        self.assertEqual (db.find_products('cat')[1][0].name, 'cat')
        self.assertEqual (db.find_products('cat')[1][0].category, 'animal')
        self.assertEqual (db.find_products('cat')[1][1].name, 'cat')
        self.assertEqual (db.find_products('cat')[1][1].category, 'petanimals')

        self.assertEqual (db.find_products( 'nope' )[0], OpResult.PRODUCT_NOT_FOUND )
        self.assertFalse (db.find_products( 'nope' )[1])
    
    def test_category_list(self):
        db = DatabaseAPI()
        product1 = Product('cat', 'animal')
        product2 = Product('cat', 'petanimals')

        self.assertEqual (db.register_new_category('animal'), OpResult.SUCCESS)
        self.assertEqual (db.register_new_category('animal'), OpResult.CATEGORY_ALREADY_EXISTS)
        self.assertEqual (db.register_new_category('petanimals'), OpResult.SUCCESS) 
        
        self.assertEqual (db.add_product(product1, 10.00, 'user'), OpResult.SUCCESS)
        self.assertEqual (db.add_product(product2, 15.00, 'user'), OpResult.SUCCESS)

        self.assertEqual (db.list_categories()[1][0], 'animal' )
        self.assertEqual (db.list_categories()[1][1], 'petanimals' )

    def test_sell_product(self):
        db = DatabaseAPI()
        product = Product('Keyboard', 'Electronics')

        self.assertEqual (db.register_new_category(product.category), OpResult.SUCCESS)
        self.assertEqual (db.add_product(product, 10.00, 'user'), OpResult.SUCCESS)
        self.assertEqual (db.make_offer(product, 15.00, 'Chuck Norris'), OpResult.SUCCESS)
        self.assertEqual (db.make_offer(product, 20.00, 'Chuck Norris'), OpResult.SUCCESS)

        self.assertEqual (db.sell_product(product)[0], OpResult.SUCCESS)
        self.assertEqual (db.sell_product(product)[1], 20.00)

        fake_product = Product('I Do not exist', 'Unkown')

        self.assertNotEqual (db.sell_product(fake_product)[0], OpResult.SUCCESS)
        self.assertEqual (db.sell_product(fake_product)[1], 0)

class ProtocolTests(unittest.TestCase):

    def test_message_packing_and_unpacking(self):
        data = ProtocolPacket(Commands.REGISTER, OpResult.SUCCESS, 'test', 'testa')
        packed_data = data.pack_data()

        unpacked_data = ProtocolPacket.unpack_data(packed_data)

        self.assertEqual(unpacked_data.cmd, Commands.REGISTER)
        self.assertEqual(unpacked_data.opresult, OpResult.SUCCESS)
        self.assertEqual(unpacked_data.arg1, 'test')
        self.assertEqual(unpacked_data.arg2, 'testa')
    
    def test_check_credentials(self):
        serverName, serverPort = 'localhost', 12000
        client = Client()
        client.connect(serverName, serverPort)

        answer = client.send_message( ProtocolPacket(Commands.OFFER, 0, 'fsf', 'pass', 10.00) )
        self.assertEqual (answer.opresult, OpResult.USER_NOT_AUTHENTICATED)

        answer = client.send_message( ProtocolPacket(Commands.LOGIN, 0, 'fsf', 'pass') )
        self.assertEqual (answer.opresult, OpResult.USER_NOT_FOUND)
        
        answer1 = client.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user', 'asdfgfdaf') )
        self.assertEqual (answer1.opresult, OpResult.INCORRECT_PASSWORD)
        
        answer = client.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user', 'pass') )
        self.assertEqual (answer.opresult, OpResult.SUCCESS)

        answer = client.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user', 'pass') )
        self.assertEqual (answer.opresult, OpResult.ALREADY_AUTHENTICATED)

        client.close_connection()
     

    def test_register_new_categories(self):
        serverName, serverPort = 'localhost', 12000
        client = Client()
        client.connect(serverName, serverPort)
        
        client.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user', 'pass'))

        answer = client.send_message( ProtocolPacket(Commands.REGISTER, 0, '', 'apple'))
        self.assertEqual (answer.opresult, OpResult.SUCCESS)

        answer = client.send_message( ProtocolPacket(Commands.REGISTER, 0, '', 'apple'))
        self.assertEqual (answer.opresult, OpResult.CATEGORY_ALREADY_EXISTS)

        answer = client.send_message( ProtocolPacket(Commands.REGISTER, 0, '', 'banana'))
        self.assertEqual (answer.opresult, OpResult.SUCCESS)

        client.close_connection()

    def test_add_product(self):
        serverName, serverPort = 'localhost', 12000
        client = Client()
        client.connect(serverName, serverPort)
        
        client.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user', 'pass'))

        client.send_message( ProtocolPacket(Commands.REGISTER, 0, '', 'animal')) 
        client.send_message( ProtocolPacket(Commands.REGISTER, 0, '', 'petanimals'))
        
        answer = client.send_message( ProtocolPacket(Commands.ADD, 0, 'cat', 'animal', 10.00))
        self.assertEqual (answer.opresult, OpResult.SUCCESS)

        answer = client.send_message( ProtocolPacket(Commands.ADD, 0, 'cat', 'petanimals', 15.00))
        self.assertEqual (answer.opresult, OpResult.SUCCESS)

        answer = client.send_message( ProtocolPacket(Commands.ADD, 0, 'cat', 'petanimals', 15.00))
        self.assertEqual (answer.opresult, OpResult.PRODUCT_ALREADY_EXISTS)

        answer = client.send_message( ProtocolPacket(Commands.ADD, 0, 'cat', 'blackhole', 15.00))
        self.assertEqual (answer.opresult, OpResult.CATEGORY_NOT_FOUND)

        client.close_connection()
        
    def test_offers(self):

        serverName, serverPort = 'localhost', 12000
        client = Client()
        client.connect(serverName, serverPort)
        
        client.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user', 'pass'))

        client.send_message( ProtocolPacket(Commands.REGISTER, 0, '', 'horses')) 
        client.send_message( ProtocolPacket(Commands.REGISTER, 0, '', 'bottles'))

        answer = client.send_message( ProtocolPacket(Commands.ADD, 0, 'stallion', 'horses', 15.00))
        answer = client.send_message( ProtocolPacket(Commands.ADD, 0, 'water', 'bottle', 10.00))

        client2 = Client()
        client2.connect(serverName, serverPort)
        
        client2.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user2', 'pass'))

        answer = client2.send_message( ProtocolPacket(Commands.OFFER, 0, 'stlion', 'horse', 10.00))
        self.assertEqual( answer.opresult,  OpResult.PRODUCT_NOT_FOUND)

        answer = client2.send_message( ProtocolPacket(Commands.OFFER, 0, 'stallion', 'horses', 10.00))
        self.assertEqual( answer.opresult,  OpResult.BID_TOO_LOW)

        answer = client2.send_message( ProtocolPacket(Commands.OFFER, 0, 'stallion', 'horses', 15.01))
        self.assertEqual( answer.opresult,  OpResult.SUCCESS)

        client.close_connection()
        client2.close_connection()

    def test_sell_product(self):
        serverName, serverPort = 'localhost', 12000
        client = Client()
        client.connect(serverName, serverPort)

        client.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user', 'pass'))
        
        product = Product('Keyboard', 'Electronics')
        
        client.send_message( ProtocolPacket(Commands.REGISTER, 0, '', product.category)) 
        client.send_message( ProtocolPacket(Commands.ADD, 0, product.name, product.category, 10.00))

        client2 = Client()
        client2.connect(serverName, serverPort)

        client2.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user2', 'pass'))
        client2.send_message( ProtocolPacket(Commands.OFFER, 0, product.name, product.category, 20.00))
       
        client3 = Client()
        client3.connect(serverName, serverPort)

        client3.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user3', 'pass'))
        client3.send_message( ProtocolPacket(Commands.OFFER, 0, product.name, product.category,  15.00))
        client3.send_message( ProtocolPacket(Commands.OFFER, 0, product.name, product.category,  21.00))

        answer = client.send_message( ProtocolPacket(Commands.SELL, 0, *product))
        self.assertEqual( answer.opresult, OpResult.SUCCESS)
        self.assertEqual( answer.price, 21.00)

        fake_product = Product('I Do not exist', 'Unkown')

        answer = client.send_message( ProtocolPacket(Commands.SELL, 0, *fake_product))
        self.assertNotEqual( answer.opresult, OpResult.SUCCESS)
        self.assertEqual( answer.price, 0)

        client.close_connection()
        client2.close_connection()
        client3.close_connection()

    def test_notifications(self):
        serverName, serverPort = 'localhost', 12000
        
        ######################Notification Listeners 
        client4 = Client()
        client4.connect(serverName, serverPort)
        client4.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user4', 'pass'))
        
        answer = client4.send_message( ProtocolPacket(Commands.NOTIFYME_ALL, 0, '', '') )
        self.assertEqual(answer.opresult, OpResult.SUCCESS)

        client5 = Client()
        client5.connect(serverName, serverPort)
        client5.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user5', 'pass'))
        
        answer = client5.send_message( ProtocolPacket(Commands.NOTIFYME_NEW_PRODUCTS, 0, '', '') )
        self.assertEqual(answer.opresult, OpResult.SUCCESS)

        client6 = Client()
        client6.connect(serverName, serverPort)
        client6.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user6', 'pass'))
        ######################
        
        client1 = Client()
        client1.connect(serverName, serverPort)
        client1.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user', 'pass'))
        
        product = Product('Keyboard', 'Electronics')
        
        client1.send_message( ProtocolPacket(Commands.REGISTER, 0, '', product.category)) 
        client1.send_message( ProtocolPacket(Commands.ADD, 0, product.name, product.category, 10.00))
        self.assertEqual( client4.last_recv_notification, "\033[94m NEW PRODUCT: Product(name='Keyboard', category='Electronics') - Start Price: 10.0 - Seller: user")
        self.assertEqual( client5.last_recv_notification, "\033[94m NEW PRODUCT: Product(name='Keyboard', category='Electronics') - Start Price: 10.0 - Seller: user")
        #self.assertEqual( client6.last_recv_notification, "\033[94m NEW PRODUCT: Product(name='Keyboard', category='Electronics') - Start Price: 10.0 - Seller: user")
        
        answer = client6.send_message( ProtocolPacket(Commands.NOTIFYME_PRODUCT_CHANGE, 0, product.name, product.category, 15) )
        self.assertEqual(answer.opresult, OpResult.SUCCESS)

        client2 = Client()
        client2.connect(serverName, serverPort)

        client2.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user2', 'pass'))
        client2.send_message( ProtocolPacket(Commands.OFFER, 0, product.name, product.category, 20.00))
        print 'TIMECHECK '+time.time().__str__()
        self.assertEqual( client4.last_recv_notification, '\x1b[94m HIGHER BID: Product: Product(name=\'Keyboard\', category=\'Electronics\') - Bid: 20.0 - Bidder: user2')
        self.assertNotEqual( client5.last_recv_notification, '\x1b[94m HIGHER BID: Product: Product(name=\'Keyboard\', category=\'Electronics\') - Bid: 20.0 - Bidder: user2')
        self.assertEqual( client6.last_recv_notification, '\x1b[94m HIGHER BID: Product: Product(name=\'Keyboard\', category=\'Electronics\') - Bid: 20.0 - Bidder: user2')



        client3 = Client()
        client3.connect(serverName, serverPort)

        client3.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user3', 'pass'))
        client3.send_message( ProtocolPacket(Commands.OFFER, 0, product.name, product.category,  15.00))
        client3.send_message( ProtocolPacket(Commands.OFFER, 0, product.name, product.category,  21.00))

        answer = client1.send_message( ProtocolPacket(Commands.SELL, 0, *product))
        self.assertEqual( answer.opresult, OpResult.SUCCESS)
        self.assertEqual( answer.price, 21.00)

        fake_product = Product('I Do not exist', 'Unkown')

        answer = client1.send_message( ProtocolPacket(Commands.SELL, 0, *fake_product))
        self.assertNotEqual( answer.opresult, OpResult.SUCCESS)
        self.assertEqual( answer.price, 0)

        client1.close_connection()
        client2.close_connection()
        client3.close_connection()
        client4.close_connection()
        client5.close_connection()
        client6.close_connection()


if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(Tests)
    # unittest.TextTestRunner(verbosity=2).run(suite)


