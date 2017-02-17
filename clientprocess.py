# pylint: disable=C0103

from client import Client

if __name__ == "__main__":
    client = Client('me')
    answer = client.send_message('localhost', 12000, ('my message1', 'gabbiani'), 1)
    print(answer[0])
    print(answer[1])

