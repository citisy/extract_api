#! -*- coding:utf-8 -*-

import re
from utils import *

tele_pt = re.compile(
    '(?:[^\d\.]|^)('  # start with num and end with num, eg: 我的电话号码是133...78，it will be matched start with 1 and end with 8
    '13[0-9]\d{8}|'  # start with 13, eg: 13312345678
    '14[579]\d{8}|'  # start with 14
    '15[0-3,5-9]\d{8}|'  # start with 15
    '166\d{8}|'  # start with 16
    '17[0-3,5-8]\d{8}|'  # start with 16
    '18[0,5-9]\d{8}|'  # start with 18
    '198\d{8}'  # start with 19
    ')(?:[^\d\.]|$)'
)


def get_telephone(text):
    """
    eg:
        >>> text = '15521323633'
        >>> telephones, text = get_telephone(text)
        >>> telephones
        >>> ['15521323633']
        >>> text
        >>> '/tele0/'
    """
    telephones = []
    i = 0

    while 1:
        telephone = tele_pt.search(text)
        if telephone is None:
            break
        text = text.replace(telephone.group(1), '/tele%d/' % i, 1)
        telephones.append(telephone.group(1))
        i += 1

    _, span_text = replace_text(text, telephones, 'tele')
    return span_text, text


if __name__ == '__main__':
    text = u'我的电话是13321323630, 你的电话号码是15521323631'
    span_text, text_ = get_telephone(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
