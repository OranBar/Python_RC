from protocol import *
from client import *
from server import *
from threading import Thread
import pytest

#Run the file "runserver.py" before running this test, or it will fail
def test_client_server_comunication():
    serverName, serverPort = 'localhost', 12000

    client = Client('dummy')
    
    client.connect(serverName, serverPort)
    answer = client.send_message( ProtocolPacket(0,0,'user','Testa') )

    assert answer.cmd == Commands.LOGIN
    assert answer.opresult == OpResult.SUCCESS