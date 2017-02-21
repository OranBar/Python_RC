from protocol import *
from client import *
from server import *
from threading import Thread
import subprocess
import unittest


class Tests(unittest.TestCase):

    def test_packing_and_unpacking(self):
        data = ProtocolPacket(Commands.REGISTER, OpResult.SUCCESS, 'test', 'testa')
        packed_data = data.pack_data()

        unpacked_data = ProtocolPacket.unpack_data(packed_data)

        self.assertEqual(unpacked_data.cmd, Commands.REGISTER)
        self.assertEqual(unpacked_data.opresult, OpResult.SUCCESS)
        self.assertEqual(unpacked_data.arg1, 'test')
        self.assertEqual(unpacked_data.arg2, 'testa')

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

if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests)
    unittest.TextTestRunner(verbosity=2).run(suite)


