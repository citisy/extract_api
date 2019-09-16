#! -*- coding:utf-8 -*-

import re
from utils import *

with open('age/age.txt', 'r', encoding='utf8') as f:
    age_str = f.read().replace('\n', '|')

age_pt = re.compile(age_str)


def get_age(text):
    ages = []
    i = 0

    while 1:
        age = age_pt.search(text)
        if age is None:
            break
        text = text.replace(age.group(0), '/age%d/' % i, 1)
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
