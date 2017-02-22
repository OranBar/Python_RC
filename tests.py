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

    def test_user_registration(self):
        db = Database()

        # serverName, serverPort = 'localhost', 12000
        # client = Client('dummy')
        # client.connect(serverName, serverPort)

        # answer = client.send_message( ProtocolPacket(Commands.REGISTER, 0, 'user','pass') )
        # self.assertEqual (answer.opresult, OpResult.SUCCESS)
        
        # answer = client.send_message( ProtocolPacket(Commands.REGISTER, 0, 'user','pass') )
        # self.assertEqual (answer.opresult, OpResult.USER_ALREADY_EXISTS)
        
        self.assertEqual (db.register_new_user('user', 'pass'), OpResult.SUCCESS)
        self.assertEqual (db.register_new_user('user', 'pass'), OpResult.USER_ALREADY_EXISTS)
    

    """
    # Run the file "runmockserver.py" before running this test, or it will fail
    def test_client_server_comunication(self):
        serverName, serverPort = 'localhost', 12000

        client = Client('dummy')

        client.connect(serverName, serverPort)
        answer = client.send_message( ProtocolPacket(0,0,'Test','Testa') )

        self.assertEqual (answer.cmd, 0)
        self.assertEqual (answer.opresult, 0)
        self.assertEqual (answer.arg1, 'TEST')
        self.assertEqual (answer.arg2, 'TESTA')
    """
    
        
    def test_check_credentials(self):
        db = Database()
        db.register_new_user('user', 'pass')

        serverName, serverPort = 'localhost', 12000
        client = Client('dummy')
        client.connect(serverName, serverPort)

        answer = client.send_message( ProtocolPacket(Commands.OFFER, 0, 'fsf', 'pass', 10.00) )
        self.assertEqual (answer.opresult, OpResult.USER_NOT_AUTHENTICATED)

        answer = client.send_message( ProtocolPacket(Commands.LOGIN, 0, 'fsf', 'pass') )
        self.assertEqual (answer.opresult, OpResult.USER_NOT_FOUND)
        
        answer = client.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user', 'asdfgfdaf') )
        self.assertEqual (answer.opresult, OpResult.INCORRECT_PASSWORD)

        answer = client.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user', 'pass') )
        self.assertEqual (answer.opresult, OpResult.SUCCESS)

        answer = client.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user', 'pass') )
        self.assertEqual (answer.opresult, OpResult.ALREADY_AUTHENTICATED)

        client.close_connection()
        
        # answer = client.send_message( ProtocolPacket(Commands.OFFER, 0, 'pazzi','gabbiani') )
        # self.assertEqual (answer.opresult, OpResult.USER_NOT_AUTHENTICATED)

        # self.assertEqual (db.check_credentials('fsf', 'pass'), OpResult.USER_NOT_FOUND)
        # self.assertEqual (db.check_credentials('user', 'asdfgfdaf'), OpResult.INCORRECT_PASSWORD)
        # self.assertEqual (db.check_credentials('user', 'pass'), OpResult.SUCCESS)
     
    def test_products_ops(self):
        db = Database()
        product1 = Product('cat', 'animal')
        product2 = Product('cat', 'petanimals')
        db.add_product(product1, 10.00)
        db.add_product(product2, 15.00)

        self.assertEqual (db.product_exists(Product('cat', 'pen')), OpResult.SUCCESS)
        self.assertEqual (db.find_products('cat')[1][0].name, 'cat')
        self.assertEqual (db.find_products('cat')[1][0].category, 'petanimals')
        self.assertEqual (db.find_products('cat')[1][1].name, 'cat')
        self.assertEqual (db.find_products('cat')[1][1].category, 'petanimals')

        self.assertEqual (db.product_exists( Product('no', 'yaw') ), OpResult.PRODUCT_NOT_FOUND)
        self.assertEqual (db.find_products( Product('no', 'yaw') )[0], OpResult.PRODUCT_NOT_FOUND )
        self.assertFalse (db.find_products( Product('no', 'yaw') )[1])
    
    def test_category_list(self):
        db = Database()
        product1 = Product('cat', 'animal')
        product2 = Product('cat', 'petanimals')
        db.add_product(product1, 10.00)
        db.add_product(product2, 15.00)

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


