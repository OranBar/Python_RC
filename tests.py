from protocol import *
from client import *
from server import *
from threading import Thread
import subprocess
import unittest



class Tests(unittest.TestCase):

    def test_message_packing_and_unpacking(self):
        data = ProtocolPacket(Commands.REGISTER, OpResult.SUCCESS, 'test', 'testa')
        packed_data = data.pack_data()

        unpacked_data = ProtocolPacket.unpack_data(packed_data)

        self.assertEqual(unpacked_data.cmd, Commands.REGISTER)
        self.assertEqual(unpacked_data.opresult, OpResult.SUCCESS)
        self.assertEqual(unpacked_data.arg1, 'test')
        self.assertEqual(unpacked_data.arg2, 'testa')

    def test_register_new_user(self):
        db = DatabaseAPI()

        for user in db.userToPass:
            print user

        self.assertEqual (db.register_new_user('user', 'pass'), OpResult.SUCCESS)
        self.assertEqual (db.register_new_user('user', 'pass'), OpResult.USER_ALREADY_EXISTS)

        # serverName, serverPort = 'localhost', 12000
        # client = Client()
        # client.connect(serverName, serverPort)

        # answer = client.send_message( ProtocolPacket(Commands.REGISTER, 0, 'user','pass') )
        # self.assertEqual (answer.opresult, OpResult.SUCCESS)
        
        # answer = client.send_message( ProtocolPacket(Commands.REGISTER, 0, 'user','pass') )
        # self.assertEqual (answer.opresult, OpResult.USER_ALREADY_EXISTS)

        # client.close_connection()
    
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
        db = Database()

        serverName, serverPort = 'localhost', 12000
        client = Client()
        client.connect(serverName, serverPort)
        print 'connected'
        
        answer = client.send_message( ProtocolPacket(Commands.REGISTER, 0, '', 'animal'))
        self.assertEqual (answer.opresult, OpResult.SUCCESS)
        print '1'

        answer = client.send_message( ProtocolPacket(Commands.REGISTER, 0, '', 'animal'))
        self.assertEqual (answer.opresult, OpResult.CATEGORY_ALREADY_EXISTS)
        print '2'

        answer = client.send_message( ProtocolPacket(Commands.REGISTER, 0, '', 'petanimals'))
        self.assertEqual (answer.opresult, OpResult.SUCCESS)
        print '3'

        client.close_connection()


    def test_add_product(self):
        db = Database()
        db.register_new_category('animal')
        db.register_new_category('animal')
        db.register_new_category('petanimals')
        product1 = Product('cat', 'animal')
        product2 = Product('cat', 'petanimals')
        product2 = Product('cat', 'blackhole')

        
        self.assertEqual (db.add_product(product1, 10.00), OpResult.SUCCESS)
        self.assertEqual (db.add_product(product2, 15.00), OpResult.SUCCESS)
        self.assertEqual (db.add_product(product2, 15.00), OpResult.PRODUCT_ALREADY_EXISTS)
        self.assertEqual (db.add_product(product3, 15.00), OpResult.CATEGORY_NOT_FOUND)
   
    def test_product_exists(self):
        db = Database()
        product1 = Product('cat', 'animal')
        product2 = Product('cat', 'petanimals')
        db.register_new_category('animal')
        db.register_new_category('petanimals')
        db.add_product(product1, 10.00)
        db.add_product(product2, 15.00)

        self.assertEqual (db.product_exists(Product('cat', 'pen')), OpResult.SUCCESS)
       
        self.assertEqual (db.product_exists( Product('no', 'yaw') ), OpResult.PRODUCT_NOT_FOUND)
       

    def test_find_products(self):
        db = Database()
        product1 = Product('cat', 'animal')
        product2 = Product('cat', 'petanimals')
        db.register_new_category('animal')
        db.register_new_category('petanimals')
        db.add_product(product1, 10.00)
        db.add_product(product2, 15.00)

        self.assertEqual (db.find_products('cat')[1][0].name, 'cat')
        self.assertEqual (db.find_products('cat')[1][0].category, 'petanimals')
        self.assertEqual (db.find_products('cat')[1][1].name, 'cat')
        self.assertEqual (db.find_products('cat')[1][1].category, 'petanimals')

        self.assertEqual (db.find_products( Product('no', 'yaw') )[0], OpResult.PRODUCT_NOT_FOUND )
        self.assertFalse (db.find_products( Product('no', 'yaw') )[1])
    
    def test_category_list(self):
        db = Database()
        product1 = Product('cat', 'animal')
        product2 = Product('cat', 'petanimals')

        self.assertEqual (db.register_new_category('animal'), OpResult.SUCCESS)
        self.assertEqual (db.register_new_category('animal'), OpResult.CATEGORY_ALREADY_EXISTS)
        self.assertEqual (db.register_new_category('petanimals'), OpResult.SUCCESS) 
        
        self.assertEqual (db.add_product(product1, 10.00), OpResult.SUCCESS)
        self.assertEqual (db.add_product(product2, 15.00), OpResult.SUCCESS)

        self.assertEqual (db.list_categories()[0], 'animal' )
        self.assertEqual (db.list_categories()[1], 'petanimals' )
        
    def test_offers(self):
        db = Database()
        product1 = Product('cat', 'animal')
        product2 = Product('cat', 'petanimals')
        db.add_product(product1, 10.00)
        db.add_product(product2, 15.00)

        self.assertEqual( db.make_offer )

if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests)
    unittest.TextTestRunner(verbosity=2).run(suite)


