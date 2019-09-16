#! -*- coding:utf-8 -*-

import re
from utils import *


qq_str = '(?:'
with open('qq/qq.txt', 'r', encoding='utf8') as f:
    qq_str += f.read().replace('\n', '|').replace('q', u'[qQ扣]')

qq_str += ')(\d{5,11})(?=\D|$)'
qq_pt = re.compile(qq_str)


def get_qq(text):
    qqs = []
    i = 0

    while 1:
        qq = qq_pt.search(text)
        if qq is None:
            break
        text = text.replace(qq.group(1), '/qq%d/' % i, 1)
        qqs.append(qq.group(1))
        i += 1

    _, span_text = replace_text(text, qqs, 'qq')
    return span_text, text


if __name__ == '__main__':
    text = u'欢迎加扣827151111'
    span_text, text_ = get_qq(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
