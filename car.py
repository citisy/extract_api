#! -*- coding:utf-8 -*-

import re
from utils import *


car_str = '(?:'
car_str += u'(?:WJ|wj)(?:[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼·•-]|[0-2][0-9][·•-]?|3[0-2][·•-]?)[消边通森金警电0-9]\d{3}[TDSHBXJtdshbxjt0-9]|'  # 武警
car_str += '(?:'
with open('car/car.txt', 'r', encoding='utf8') as f:
    car_str += f.read().replace('\n', '|')

car_str += u'|)[·•]?(?:'
car_str += '(?:[DFdf][A-HJ-NP-Za-hj-np-z0-9]\d{4})|(?:\d{5}[DFdf])|'    # 新能源
car_str += '[A-HJ-NP-Za-hj-np-z0-9]{5}|'  # 常规车牌号
car_str += u'[A-Da-d0-9]\d{3}警'  # 警车
car_str += ')|'
car_str += u'\d{6}使|'  # 大使馆
car_str += u'(?:[沪粤川云桂鄂陕蒙藏黑辽渝][Aa]|鲁[Bb]|闽[Dd]|蒙[Ee]|蒙[Hh])\d{4}领|'  # 领事馆
car_str += u'[军空海北沈兰济南广成甲乙丙丁庚辛壬寅辰戍午未申VZKHBSLJNGCEvzkhbsljngce][A-DJ-PR-TVYa-dj-pr-tvy][·•-]?\d{5}'   # 军用
car_str += u')(?=[^A-Za-z0-9警领使]|$)'    # 特殊车


def get_car(text):
    cars = []
    i = 0

    while 1:
        car = re.search(car_str, text)
        if car is None:
            break
        text = text.replace(car.group(0), '/car%d/' % i, 1)
        cars.append(car.group(0))
        i += 1

    _, span_text = replace_text(text, cars, 'car')
    return span_text, text


if __name__ == '__main__':
    text = u'我开着粤B12345走在幸福的大道上'
    span_text, text_ = get_car(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
