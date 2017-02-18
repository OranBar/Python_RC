from protocol import *


class Database(object):

    userToPass = {'user':'pass'}

    def register_new_user(self, username, password):
        userToPass[username] = password
    

    def check_credentials(self, username, password):
        if username in self.userToPass:
            if self.userToPass[username] == password:
                return OpResult.SUCCESS
            else:
                return OpResult.INVALID_PASSWORD
        else:
            return OpResult.INVALID_USERNAME