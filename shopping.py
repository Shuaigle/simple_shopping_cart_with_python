import sys
import re
import datetime
from decimal import Decimal


class Electronic_products:
    '''
    電子
    '''
    def __init__(self):
        self.products = ["顯示器", "ipad", "iphone", "螢幕", "筆記型電腦", "鍵盤"]
        self.name = "電子"


class Food:
    '''
    食品
    '''
    def __init__(self):
        self.products = ["麵包", "蛋糕", "牛肉", "魚", "蔬菜"]
        self.name = "食品"


class Groceries:
    '''
    日用品
    '''
    def __init__(self):
        self.products = ["餐巾紙", "收納箱", "咖啡杯", "雨傘"]
        self.name = "日用品"


class Alcoholic_drink:
    '''
    酒類
    '''
    def __init__(self):
        self.products = ["啤酒", "白酒", "伏特加"]
        self.name = "酒類"


def split_txt(lines):
    '''
    將字串分離
    '''
    i = 0
    for line in lines:
        line = re.split(r":|\*|\||\n|\s", line)
        if '' in line: line.remove('')
        lines[i] = line
        i += 1


def validate(date_text):
    '''
    檢查是否為時間格式

    回傳boolean
    '''
    res = True
    try:
        res = bool(datetime.datetime.strptime(date_text, '%Y.%m.%d'))
    except ValueError:
        res = False
    except TypeError:
        res = False
    return res


def festival_discount(lines, discount_categories):
    '''
    處理節慶折扣
    確認是否存在節慶日期、日期格式是否正確、日期是否與結帳日期相符

    回傳折扣、折扣分類的物件
    '''
    isFestivalDate = lines[0][0]
    isToday = lines[-2][0]
    if (validate(isFestivalDate)) and (isFestivalDate == isToday):
        discount = lines[0][1]
        discount_category = discount_categories.get(lines[0][2])
    else:
        discount = 1
        discount_category = None
    check_discount_value(discount)
    return discount, discount_category

def sum_up_products(lines, discount, discount_category):
    '''
    依據折扣加總金額

    回傳總金額
    '''
    res = 0
    for line in lines:
        # 尋找非日期格式且長度大於1，即第1筆消費資訊
        if not validate(line[0]) and \
        len(line) > 1:
            units = line[0]
            product = line[1]
            price = line[2]

            if discount_category is not None and product in discount_category.products:
                price = Decimal(price) * Decimal(discount)
            check_units(units)
            check_product_price(price)
            res = round(Decimal(res) + Decimal(units) * Decimal(price), 2)
    return res

def coupon_stage(lines, sum):
    '''
    處理折價券
    1. 確認折價券存在(日期格式、長度)
    2. 確認時限內使用
    3. 確認金額符合預期

    回傳折價後金額
    '''
    isInsideDiscountDate = lines[-1][0]
    isToday = lines[-2][0]

    if validate(isInsideDiscountDate) and \
        len(lines[-1]) > 1 and \
        datetime.datetime.strptime(isToday, '%Y.%m.%d') <=  datetime.datetime.strptime(isInsideDiscountDate, '%Y.%m.%d')and \
        Decimal(lines[-1][1]) <= sum: # 判斷折價券是否消費滿額，檢查日期是否符合
        discount = lines[-1][2]
        sum -= Decimal(discount) # 進行折價
    return sum


# 邊界條件
def check_discount_value(discount):
    discount = Decimal(discount)
    if discount < 0 or discount > 1:
        raise ValueError('折扣須介於 0-1 之間')


def check_units(units):
    if not units.isdigit():
        raise ValueError('數量需為正整數')
    if int(units) == 0:
        raise ValueError('數量不可為0')
    return True


def check_product_price(price):
    if Decimal(price) < 0:
        raise ValueError('價格不可為負')
    

def main():
    # 參數
    sum = 0
    discount_categories = {
        "電子": Electronic_products(),
        "食品": Food(),
        "日用品": Groceries(),
        "酒類": Alcoholic_drink()
    }

    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()

        # 將文件檔內容拆分
        split_txt(lines)

        # 處理節慶折價資訊
        discount, discount_category = festival_discount(lines, discount_categories)

        # 加總商品價格
        sum = sum_up_products(lines, discount, discount_category)
        
        # 處理折價券
        sum = coupon_stage(lines, sum)

        print(sum)


if __name__ == '__main__':
    main()
