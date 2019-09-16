#! -*- coding:utf-8 -*-

import re
from utils import *

percent_pt = re.compile('\d+(?:\.\d+)?[%‰]|10{2,4}[分份]之?\d+(?:[\.点]\d+)?')


def get_percent(text):
    text_ = text
    text, r = replace_num(text)

    percents = []
    i = 0
    while 1:
        percent = percent_pt.search(text)
        if percent is None:
            break
        text = text.replace(percent.group(0), '/percent%d/' % i, 1)
        percents.append(percent.group(0))
        i += 1

    restore_num(text_, percents, r)

    _, span_text = replace_text(text, percents, 'percent')
    return span_text, text


if __name__ == '__main__':
    text = u'100%, 0.5%, 百分之零点五'
    span_text, text_ = get_percent(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
