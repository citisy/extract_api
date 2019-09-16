#! -*- coding:utf-8 -*-

import re
import codecs
from utils import *


z = '\d+(?:\.\d{1,2})?'
y = '\d+'
money_str = ''
with open('money/money.txt', 'r', encoding='utf8') as f:
    money_str += f.read().replace('\n', '|').replace('z', z).replace('y', y)
money_pt = re.compile(money_str)


def get_money(text):
    """
    eg:
        >>> text = u'我有壹佰块钱，我给你一块。'
        >>> moneys, text = get_money(text)
        >>> moneys
        >>> [u'6块', u'1块']
        >>> text
        >>> u'我有/money0/钱，我给你/money1/。'
    """
    text_ = text
    text, r = replace_num(text)
    moneys = []
    i = 0

    while 1:
        money = money_pt.search(text)
        if money is None:
            break
        text = text.replace(money.group(0), '/money%d/' % i, 1)
        moneys.append(money.group(0))
        i += 1

    restore_num(text_, moneys, r)

    _, span_text = replace_text(text, moneys, 'money')
    return span_text, text


if __name__ == '__main__':
    text = u'我有壹仟零一块钱，我给你壹佰块，88。'
    span_text, text_ = get_money(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
