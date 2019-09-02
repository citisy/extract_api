#! -*- coding:utf-8 -*-

import re
from rep_tools import *


def get_stamp(text):
    stamps = []
    i = 0

    while 1:
        stamp = re.search(
            u'(?:邮证?编码?[：:是]?)(\d{6})(?=\D|$)',
            text
        )
        if stamp is None:
            break
        text = text.replace(stamp.group(1), '/stamp%s/' % str(i), 1)
        stamps.append(stamp.group(1))
        i += 1

    _, span_text = replace_text(text, stamps, 'stamp')
    return span_text, text


if __name__ == '__main__':
    text = u'邮编510009'
    span_text, text_ = get_stamp(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
