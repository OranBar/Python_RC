from protocol import *
from client import *
from server import *
from threading import Thread
import pytest

#Run the file "runserver.py" before running this test, or it will fail
def test_authentication():
    serverName, serverPort = 'localhost', 12000

    client = Client('dummy')
    
    client.connect(serverName, serverPort)

    answer = client.send_message( ProtocolPacket(Commands.OFFER, 0, 'pazzi','gabbiani') )

    assert answer.cmd != Commands.LOGIN
    assert answer.opresult == OpResult.USER_NOT_AUTHENTICATED
    
    answer = client.send_message( ProtocolPacket(Commands.LOGIN, 0,'pazzi','gabbiani') )
    
    assert answer.cmd == Commands.LOGIN
    assert answer.opresult == OpResult.INVALID_USERNAME

    answer = client.send_message( ProtocolPacket(Commands.LOGIN, 0,'user','gabbiani') )
    
    assert answer.cmd == Commands.LOGIN
    assert answer.opresult == OpResult.INVALID_PASSWORD

    answer = client.send_message( ProtocolPacket(Commands.LOGIN, 0, 'user','pass') )

    assert answer.cmd == Commands.LOGIN
    assert answer.opresult == OpResult.SUCCESS

    client.close_connection()