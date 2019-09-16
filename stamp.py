#! -*- coding:utf-8 -*-

import re
from utils import *

stamp_pt = re.compile('(?:邮证?编码?[：:是]?)(\d{6})(?=\D|$)')


def get_stamp(text):
    stamps = []
    i = 0

    while 1:
        stamp = stamp_pt.search(text)
        if stamp is None:
            break
        text = text.replace(stamp.group(1), '/stamp%d/' % i, 1)
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
