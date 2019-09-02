#! -*- coding:utf-8 -*-

import re
from rep_tools import *


def get_percent(text):
    text_ = text
    text = text.replace(
        u'一', '1').replace(u'二', '2').replace(u'三', '3').replace(u'四', '4').replace(u'五', '5').replace(
        u'六', '6').replace(u'七', '7').replace(u'八', '8').replace(u'九', '9').replace(u'两', '2').replace(u'零', '0')

    text = re.sub(u'([十百千万亿]?(?:\d+(?:[\.点]\d+)?[十百千万亿]*)+\d*)+|[十百千万亿]', replace_num, text)

    percents = []
    i = 0
    while 1:
        percent = re.search(
            u'\d+(?:\.\d+)?[%‰]|10{2,4}[分份]之?\d+(?:[\.点]\d+)?',
            text
        )
        if percent is None:
            break
        text = text.replace(percent.group(0), '/percent%s/' % str(i), 1)
        percents.append(percent.group(0))
        i += 1

    x = 0
    for i in r:
        for j in range(x, len(percents)):
            if i[1] in percents[j]:
                percents[j] = percents[j].replace(i[1], text_[i[0][0]:i[0][1]], 1)
                x = j
                break

    _, span_text = replace_text(text, percents, 'percent')
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
    text = u'100%, 0.5%, 百分之零点五'
    span_text, text_ = get_percent(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
