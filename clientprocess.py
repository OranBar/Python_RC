# pylint: disable=C0103

from client import Client

client = Client('me')
answer = client.send_message('localhost', 12000, 'my message', 1)
print answer

