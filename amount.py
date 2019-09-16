#! -*- coding:utf-8 -*-

import re
from utils import *

amount_str = u'\d+(?:\.\d+|多|余)?(?:'
with open('amount/amount.txt', 'r', encoding='utf8') as f:
    amount_str += f.read().replace('\n', '|')
amount_str += ')'
amount_str = amount_str[:-1] + ')'
amount_pt = re.compile(amount_str)


def get_amount(text):
    text_ = text
    text, r = replace_num(text)

    amounts = []
    i = 0
    while 1:
        amount = amount_pt.search(text)
        if amount is None:
            break
        text = text.replace(amount.group(0), '/amount%d/' % i, 1)
        amounts.append(amount.group(0))
        i += 1

    restore_num(text_, amounts, r)

    _, span_text = replace_text(text, amounts, 'amount')
    return span_text, text


if __name__ == '__main__':
    text = u'一袋苹果两只梨'
    span_text, text_ = get_amount(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
