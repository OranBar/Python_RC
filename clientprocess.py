# pylint: disable=C0103

from client import Client

client = Client('me')
client.connect('localhost', 12000)

