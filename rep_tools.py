#! -*- coding: utf-8 -*-

import re
import os


def replace_text(text, li, s):
    """
    eg:
        text=报警电话是110, li=[110], s=phone, flag=0 => return ->  报警电话是110/phone/
        text=我有/money0/, li=[110元], s=money, flag=1 => return -> 我有110元/money/
    """
    span_text = {}
    for i, l in enumerate(li):
        if l == '':
            continue
        text_ = re.search('/%s%s/' % (s, str(i)), text)
        if text_:
            text = text.replace('/%s%s/' % (s, str(i)), l, 1)
            span = text_.span()
            span_text[(span[0], span[0]+len(l))] = s
    return text, span_text


def abs_path(path):
    return os.path.join(os.path.dirname(__file__), path) 
