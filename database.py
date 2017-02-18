from protocol import *
import pickle


class Database(object):

    userToPass = {'user':'pass'}
    products = []

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

    def add_product(self, product):
        if (product in self.products):
            return OpResult.PRODUCT_ALREADY_EXISTS
        
        self.products.append(product)
        return OpResult.SUCCESS

    def product_exists(self, product):
        if product in self.products:
            return OpResult.SUCCESS
        else: 
            return OpResult.PRODUCT_NOT_FOUND

    def find_products(self, productName):
        return filter(lambda p: p[0]==productName, self.products)

    def list_category(self, categoryName):
        return filter(lambda p: p[0]==categoryName, self.products)

    def list_categories(self):
        return map(lambda p: p[0], self.products)

    def save(self):
        pickle.dump(self, open( "db.p", "wb" ))