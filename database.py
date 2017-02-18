from protocol import *
import pickle


class Database(object):

    userToPass = { 'user':'pass' }
    
    categories = ['category1']
    #products = [('product1', 'category1')]
    
    offers = { ('product1', 'category1'):10 }

    def register_new_user(self, username, password):
        userToPass[username] = password
    
    def is_valid(self, str):
        #TODO: implement me (remove all spaces, check length >=3)
        return True

    def check_credentials(self, username, password):
        if not self.is_valid(username):
            return OpResult.INVALID_PRODUCT_NAME
        if not self.is_valid(password):
            return OpResult.INVALID_PASSWORD
            
        if username in self.userToPass:
            if self.userToPass[username] == password:
                return OpResult.SUCCESS
            else:
                return OpResult.INVALID_PASSWORD
        else:
            return OpResult.INVALID_USERNAME

    def register_new_category(self, categoryName):
        if not self.is_valid(categoryName):
            return OpResult.INVALID_CATEGORY_NAME

        if(categoryName not in self.categories):
            self.categories.append(categoryName)
            return OpResult.SUCCESS
        else:
            return OpResult.CATEGORY_ALREADY_EXISTS

    # Add minimum price
    def add_product(self, product, startPrice):
        if not self.is_valid(product[0]):
            return OpResult.INVALID_PRODUCT_NAME
        if not self.is_valid(product[1]):
            return OpResult.INVALID_CATEGORY_NAME

        if (product in self.offers.keys):
            return OpResult.PRODUCT_ALREADY_EXISTS
        
        self.products.append(product)
        return OpResult.SUCCESS

    def product_exists(self, product):
        if not self.is_valid(product[0]):
            return OpResult.INVALID_PRODUCT_NAME

        if product in self.products:
            return OpResult.SUCCESS
        else: 
            return OpResult.PRODUCT_NOT_FOUND

    def find_products(self, productName):
        if not self.is_valid(productName):
            return OpResult.INVALID_PRODUCT_NAME

        return (OpResult.SUCCESS, filter(lambda p: p[0]==productName, self.offers.keys))

    def list_products_in_category(self, categoryName):
        if not self.is_valid(productName):
            return OpResult.INVALID_CATEGORY_NAME

        return (OpResult.SUCCESS, filter(lambda p: p[1]==categoryName, self.offers.keys))

    def list_categories(self):
        return categories

    def make_offer(self, product, price):
        #TODO
        if (*product, price) in self.offers:
            self.products


    # def save(self):
    #     pickle.dump(self, open( "db.p", "wb" ))