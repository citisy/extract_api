#! -*- coding:utf-8 -*-

import re
import codecs
from rep_tools import *


fp = 'money/money.txt'
z = '\d+(?:\.\d{1,2})?'
y = '\d+'
money_str = u''
for line in codecs.open(fp, 'r', encoding='utf8'):
    money_str += line.rstrip('\n').strip().replace('z', z).replace('y', y) + '|'

money_str = money_str[:-1]
money_str = re.compile(money_str)


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
    text = text.replace(
        u'壹', '1').replace(u'贰', '2').replace(u'叁', '3').replace(u'肆', '4').replace(u'伍', '5').replace(
        u'陆', '6').replace(u'柒', '7').replace(u'捌', '8').replace(u'玖', '9').replace(u'拾', u'十').replace(
        u'佰', u'百').replace(u'仟', u'千').replace(
        u'一', '1').replace(u'二', '2').replace(u'三', '3').replace(u'四', '4').replace(u'五', '5').replace(
        u'六', '6').replace(u'七', '7').replace(u'八', '8').replace(u'九', '9').replace(u'两', '2').replace(u'零', '0')
    text = re.sub(u'([十百千万亿]?(?:\d+(?:[\.点]\d+)?[十百千万亿]*)+\d*)+|[十百千万亿]', replace_num, text)
    moneys = []
    i = 0

    while 1:
        money = re.search(money_str, text)
        if money is None:
            break
        text = text.replace(money.group(0), '/money%s/' % str(i), 1)
        moneys.append(money.group(0))
        i += 1

    x = 0
    for i in r:
        for j in range(x, len(moneys)):
            if i[1] in moneys[j]:
                moneys[j] = moneys[j].replace(i[1], text_[i[0][0]:i[0][1]], 1)
                x = j
                break

    _, span_text = replace_text(text, moneys, 'money')
    return span_text, text


r = []
def replace_num(text_):
    """
    step:
        * replace chinese num, eg: 这次的金钱是十一亿二千三十四万五千六百零七块 -> 这次的金钱是十1亿2千3十4万5千6百07点8块
        * find num str, eg: 这次的金钱是十一亿二千三十四万五千六百零七块 -> 十1亿2千3十4万5千6百07点8
        * replace u'百千万亿u', eg: 十1亿2千314万5千6百07 -> 11023145607.8
    ---------
    eg:
        >>> text = u'十一亿二千三十四万五千六百零七点八'
        >>> replace_num(text)
        >>> 11023145607.8
    """
    span = text_.span()
    text = text_.group()
    num = 0
    shi, bai, qian, wan, yi = [1] * 5
    d = 1
    for i in text[::-1]:
        try:  # when i is int type
            num += int(i) * d * shi * bai * qian * wan * yi
            d *= 10
        except:  # when type is str type, eg: 十百千万亿
            if i == u'十':
                shi *= 10
            if i == u'百':
                shi = 1
                bai *= 100
            if i == u'千':
                shi, bai = [1] * 2
                qian *= 1000
            if i == u'万':
                shi, bai, qian = [1] * 3
                wan *= int(1e4)
            if i == u'亿':
                shi, bai, qian, wan = [1] * 4
                yi *= int(1e8)
            if i == '.' or i == u'点':
                if num < d:
                    num /= d
                else:
                    num //= d
            d = 1

    if d == 1:  # when d = 1, meaning that the last operation didnu't be added, eg: 十1亿, operation u'十' will be ignored
        num += 1 * d * shi * bai * qian * wan * yi

    r.append([span, str(num)])
    return str(num)


if __name__ == '__main__':
    text = u'我有壹仟零一块钱，我给你壹佰块，88。'
    span_text, text_ = get_money(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
