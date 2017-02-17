from protocol import *
import pytest

def test_packing_and_unpacking():
    data = ProtocolPacket(Commands.REGISTER, OpResult.SUCCESS, 'test', 'testa')
    packed_data = data.pack_data()

    unpacked_data = ProtocolPacket.unpack_data(packed_data)

    assert unpacked_data.cmd == Commands.REGISTER
    assert unpacked_data.opresult == OpResult.SUCCESS
    assert unpacked_data.arg1 == 'test'
    assert unpacked_data.arg2 == 'testa'




