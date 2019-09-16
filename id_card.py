#! -*- coding:utf-8 -*-

import re
import codecs
from utils import *


idcard_set = set()
for line in codecs.open('id_card/id.txt', 'r', encoding='utf8'):
    idcard_set.add(line[:3])


def get_idcard(text):
    """
    eg:
        >>> text = '44078219991111777x'
        >>> idcards, text = get_idcard(text)
        >>> idcards
        >>> ['44078219991111777x']
        >>> text
        >>> '/idcard0/'
    """
    idcards = []
    i = 0

    while 1:
        idcard = re.search(
            '(?:[^\d\.]|^)(\d{17}[\dXx])(?:[^\d\.]|$)', text  # 17-bit nums + 1-bit nums or x\X
        )
        if idcard is None:
            break
        text = text.replace(idcard.group(1), '/idcard%s/' % str(i), 1)
        idcards.append(idcard.group(1))
        i += 1

    for i, id_ in enumerate(idcards):   # judge the first 3 bit
        if id_[:3] not in idcard_set:
            text = text.replace('/idcard%s/' % str(i), idcards[i], 1)
            idcards[i] = ''

    _, span_text = replace_text(text, idcards, 'idcard')
    return span_text, text


if __name__ == '__main__':
    text = '我的身份证44078219991111777x'
    span_text, text_ = get_idcard(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
