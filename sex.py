#! -*- coding:utf-8 -*-

import re
from rep_tools import *


def get_sex(text):
    sexes = []
    i = 0

    while 1:
        sex = re.search(
            u'男|先生|叔叔|哥哥|GG|gg|女|小姐|阿姨|姐姐|妹子|MM|mm',
            text
        )
        if sex is None:
            break
        text = text.replace(sex.group(0), '/sex%s/' % str(i), 1)
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
