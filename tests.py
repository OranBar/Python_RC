from protocol import *
from client import *
from server import *
from threading import Thread
import pytest
import subprocess


def test_packing_and_unpacking():
    data = ProtocolPacket(Commands.REGISTER, OpResult.SUCCESS, 'test', 'testa')
    packed_data = data.pack_data()

    unpacked_data = ProtocolPacket.unpack_data(packed_data)

    assert unpacked_data.cmd == Commands.REGISTER
    assert unpacked_data.opresult == OpResult.SUCCESS
    assert unpacked_data.arg1 == 'test'
    assert unpacked_data.arg2 == 'testa'

#Run the file "runmockserver.py" before running this test, or it will fail
def test_client_server_comunication():
    serverName, serverPort = 'localhost', 12000

    client = Client('dummy')
    
    client.connect(serverName, serverPort)
    answer = client.send_message( ProtocolPacket(0,0,'Test','Testa') )

    assert answer.cmd == 0
    assert answer.opresult == 0
    assert answer.arg1 == 'TEST'
    assert answer.arg2 == 'TESTA'



    



