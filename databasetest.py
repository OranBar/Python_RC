from database import *
import pytest

def test_check_credentials():
    db = Database()
    assert db.check_credentials('user', 'pass') == OpResult.SUCCESS

def test_products_ops():
    db = Database()
    product = ('cat', 'pen')
    db.add_product(product, 10.00)
    assert db.product_exists(('cat', 'pen')) == OpResult.SUCCESS
    assert db.find_products('cat')[1] == 'cat'
    assert db.find_products('cat')[1][1] == 'pen'

    product2 = ('no', 'yaw')
    assert db.product_exists(('no', 'yaw')) == OpResult.PRODUCT_NOT_FOUND

    






