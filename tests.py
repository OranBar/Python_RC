from protocol import *
from client import *
from server import *
from threading import Thread
import pytest

def test_packing_and_unpacking():
    data = ProtocolPacket(Commands.REGISTER, OpResult.SUCCESS, 'test', 'testa')
    packed_data = data.pack_data()

    unpacked_data = ProtocolPacket.unpack_data(packed_data)

    assert unpacked_data.cmd == Commands.REGISTER
    assert unpacked_data.opresult == OpResult.SUCCESS
    assert unpacked_data.arg1 == 'test'
    assert unpacked_data.arg2 == 'testa'

def client_server_comunication():
    serverName, serverPort = 'localhost', 12000
    
    client = Client('dummy')
    
    answer = client.send_message(serverName, serverPort, ProtocolPacket(0,0,'Test','Testa'))

    assert answer.arg1 == 'Test'
    assert answer.arg2 == 'Testa'
    



