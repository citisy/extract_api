#! -*- coding:utf-8 -*-

import re
from rep_tools import *


def get_age(text):
    ages = []
    i = 0

    while 1:
        age = re.search(
            u'\d{1,3}岁|而立|不惑|知天?命|花甲|耳顺|古稀|鲐背|耄耋|期颐',
            text
        )
        if age is None:
            break
        text = text.replace(age.group(0), '/age%s/' % str(i), 1)
        ages.append(age.group(0))
        i += 1

    _, span_text = replace_text(text, ages, 'age')
    return span_text, text


if __name__ == '__main__':
    text = u'我今年30岁'
    span_text, text_ = get_age(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
