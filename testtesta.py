from protocol import *

data = ProtocolPacket(Commands.REGISTER, OpResult.SUCCESS, 'test', 'testa')
packed_data = data.pack_data()

unpacked_data = ProtocolPacket.unpack_data(packed_data)

print unpacked_data.cmd
print unpacked_data.opresult
print unpacked_data.arg1
print unpacked_data.arg2









# s = 'testtesta'
# s = bytes(s)    # Or other appropriate encoding
# packed_data = struct.pack("I I %ds" % (len(s),), len(s), Commands.NOTIFYME, s)

# (i, op), data = struct.unpack("I I", packed_data[:8]), packed_data[8:]
# s, data = data[:i], data[i:]

# print op
