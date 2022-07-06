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
    '''
    if (validate(lines[0][0])) and (lines[0][0] == lines[-2][0]):
        discount = lines[0][1]
        discount_category = discount_categories.get(lines[0][2])
    else:
        discount = 1
        discount_category = None
    return discount, discount_category

def sum_up_products(lines, discount, discount_category):
    '''
    依據折扣加總金額
    '''
    res = 0
    for line in lines:
        # 尋找非日期格式且長度大於1，即第1筆消費資訊
        if not validate(line[0]) and \
        len(line) > 1:
            if discount_category is not None and line[1] in discount_category.products:
                line[2] = Decimal(line[2]) * Decimal(discount)
            res = round(Decimal(res) + Decimal(line[0]) * Decimal(line[2]), 2)
    return res

def coupon_stage(lines, sum):
    '''
    處理折價券
    1. 確認折價券存在(日期格式、長度)
    2. 確認時限內使用
    3. 確認金額符合預期
    '''
    if validate(lines[-1][0]) and \
        len(lines[-1]) > 1 and \
        datetime.datetime.strptime(lines[-2][0], '%Y.%m.%d') <=  datetime.datetime.strptime(lines[-1][0], '%Y.%m.%d')and \
        Decimal(lines[-1][1]) <= sum: # 判斷折價券是否消費滿額，檢查日期是否符合
        sum = sum - Decimal(lines[-1][2]) # 進行折價
    return sum

def main():
    # 參數
    sum = 0
    discount_categories = {
        "電子": Electronic_products(),
        "食品": Food(),
        "日用品": Groceries(),
        "酒類": Alcoholic_drink()
    }

    while True:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()

            # 將文件檔內容拆分
            split_txt(lines)

            # 處理節慶折價資訊
            discount, discount_category = festival_discount(lines, discount_categories)

            # 加總商品價格
            sum = sum_up_products(lines, discount, discount_category)
            
            # 處理折價券
            # 日期格式 -> 長度 -> 有效期限內 -> 金額符合折價條件 -> 折價
            sum = coupon_stage(lines, sum)

            print(sum)
            break


if __name__ == '__main__':
    main()
