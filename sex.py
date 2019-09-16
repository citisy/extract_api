#! -*- coding:utf-8 -*-

import re
from utils import *

with open('sex/sex.txt', 'r', encoding='utf8') as f:
    sex_str = f.read().replace('\n', '|')
sex_pt = re.compile(sex_str)


def get_sex(text):
    sexes = []
    i = 0

    while 1:
        sex = sex_pt.search(text)
        if sex is None:
            break
        text = text.replace(sex.group(0), '/sex%d/' % i, 1)
        sexes.append(sex.group(0))
        i += 1

    _, span_text = replace_text(text, sexes, 'sex')
    return span_text, text


if __name__ == '__main__':
    text = u'我是男的'
    span_text, text_ = get_sex(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
