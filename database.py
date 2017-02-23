from protocol import *
import pickle


class DatabaseAPI(object):

    userToPass = {}
    categories = []
    offers = {}

    # This example shows in what form the database will store items
    # userToPass = { 'user' : 'pass' }
    # categories = ['category1']
    # offers = { ('product1', 'category1') : (10.00, 'user') }

    def __init__(self):
        self.userToPass = {}
        self.categories = []
        self.offers = {} 


    def is_valid_username(self, str):
        return self.is_valid(str)

    def is_valid_password(self, str):
        return self.is_valid(str)

    def is_valid_product(self, str):
        return self.is_valid(str)

    def is_valid_category(self, str):
        return self.is_valid(str)

    def is_valid(self, str):
        #Remove all spaces, then check length >=3
        return len(str.replace(" ", "")) >= 3

    def register_new_user(self, username, password):
        if not self.is_valid_username(username):
            return OpResult.INVALID_USERNAME
        if not self.is_valid_password(password):
            return OpResult.INVALID_PASSWORD
        if username in self.userToPass:
            return OpResult.USER_ALREADY_EXISTS

        self.userToPass[username] = password
        return OpResult.SUCCESS

    def check_credentials(self, username, password):
        if not self.is_valid_username(username):
            return OpResult.INVALID_USERNAME
        if not self.is_valid_password(password):
            return OpResult.INVALID_PASSWORD
            
        if username in self.userToPass:
            if self.userToPass[username] == password:
                return OpResult.SUCCESS
            else:
                return OpResult.INCORRECT_PASSWORD
        else:
            return OpResult.USER_NOT_FOUND

    def register_new_category(self, categoryName):
        if not self.is_valid_category(categoryName):
            return OpResult.INVALID_CATEGORY_NAME

        if(categoryName not in self.categories):
            self.categories.append(categoryName)
            return OpResult.SUCCESS
        else:
            return OpResult.CATEGORY_ALREADY_EXISTS

    # Add minimum price
    def add_product(self, product, startPrice):
        if not self.is_valid_product(product.name):
            return OpResult.INVALID_PRODUCT_NAME
        if not self.is_valid_category(product.category):
            return OpResult.INVALID_CATEGORY_NAME

        if product.category not in self.categories:
            return OpResult.CATEGORY_NOT_FOUND
        # if (product in self.offers.keys):
        if (product in self.offers):
            return OpResult.PRODUCT_ALREADY_EXISTS
        
        self.offers[product] = startPrice
        return OpResult.SUCCESS

    def product_exists(self, product):
        if not self.is_valid_product(product[0]):
            return OpResult.INVALID_PRODUCT_NAME

        if product in self.offers:
            return OpResult.SUCCESS
        else: 
            return OpResult.PRODUCT_NOT_FOUND

    def find_products(self, productName):
        if not self.is_valid_product(productName):
            return (OpResult.INVALID_PRODUCT_NAME, None)

        result = filter(lambda p: p[0]==productName, self.offers)
        if len(result) > 0:
            return (OpResult.SUCCESS, result)
        else:
            return (OpResult.PRODUCT_NOT_FOUND, [])
            

    def list_products_in_category(self, categoryName):
        if not self.is_valid_product(productName):
            return OpResult.INVALID_CATEGORY_NAME

        result = filter(lambda p: p[1]==categoryName, self.offers.keys)
        if len(result) > 0:
            return (OpResult.SUCCESS, result)
        else:
            return (OpResult.CATEGORY_NOT_FOUND, [])

    def list_categories(self):
        return (OpResult.SUCCESS, categories)

    def make_offer(self, product, price):
        if product not in self.offers:
            return OpResult.PRODUCT_NOT_FOUND
        
        if offers[product] >= price:
            return OpResult.BID_TOO_LOW
        else: 
            offers[product] = price
            return OpResult.SUCCESS

