from shopping import (
    split_txt, 
    validate, 
    festival_discount, 
    sum_up_products,
    coupon_stage
)
from shopping import Electronic_products, Food, Groceries, Alcoholic_drink
import pytest
from decimal import Decimal


@pytest.fixture
def discount_categories():
    '''
    測試資料 分類
    '''
    return {
            "電子": Electronic_products(),
            "食品": Food(),
            "日用品": Groceries(),
            "酒類": Alcoholic_drink()
    }

@pytest.fixture
def lines():
    '''
    測試資料 行
    '''
    return \
        [['2015.11.11', '0.7', '電子'], [''], 
        ['1', 'ipad', '2399.00'], 
        ['1', '顯示器', '1799.00'], 
        ['12', '啤酒', '25.00'], 
        ['5', '麵包', '9.00'], 
        [''], 
        ['2015.11.11'], 
        ['2016.3.2', '1000', '200']]

def test_split_txt():
    lines = ["2015.11.11|0.7|電子", "1*ipad:2399.00"]
    split_txt(lines)
    assert lines == [["2015.11.11", "0.7", "電子"], ["1", "ipad", "2399.00"]]

def test_validate():
    date = "1818.11.11"
    ndate = "1818.13.13"
    nndate = "1235325"
    nnndate = 123123

    assert validate(date) == True
    assert validate(ndate) == False
    assert validate(nndate) == False
    assert validate(nnndate) == False

def test_festival_discount(discount_categories):
    lines = [["2015.11.11", "0.7", "電子"], ["1", "ipad", "2399.00"]]
    discount_categories = discount_categories
    discount, discount_category = festival_discount(lines, discount_categories)
    assert (discount, discount_category.name) == ("0.7", "電子")
    
def test_sum_up_products():
    lines = [["1", "ipad", "2399.00"], ["1", "ipad", "2399.00"]]
    discount = 0.1
    discount_category = Electronic_products()
    assert sum_up_products(lines, discount, discount_category) == Decimal('479.80')

def test_coupon_stage(lines):
    sum = Decimal('1123.12')
    assert coupon_stage(lines, sum) == Decimal('923.12')
