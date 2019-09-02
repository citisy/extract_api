#! -*- coding:utf-8 -*-

import re
import codecs
from rep_tools import *


phone_str = '(?:[^\d\.]|^)((?:'
for line in codecs.open('phone/internation.txt', 'r', encoding='utf8'):
    phone_str += '00' + line.replace('\n', '').replace(' ', '') + '|'

phone_str = phone_str[:-1] + ')-\d{7,8}|(?:'  # international phone

for line in codecs.open('phone/nation.txt', 'r', encoding='utf8'):
    phone_str += line.replace('\n', '').replace(' ', '') + '|'

phone_str = phone_str[:-1] + ')?[-]?[2-8]\d{6,7}|'  # chinese phone

for line in codecs.open('phone/special.txt', 'r', encoding='utf8'):  # special phone, eg: 110
    phone_str += line.replace('\n', '').replace(' ', '') + '|'

phone_str += '[48]00-?\d{7,8}|[48]00\d-\d{3}-\d{3}|[48]00-\d{3}-\d{4}|9[56]\d{3})(?:[^\d\.]|$)'
phone_str = re.compile(phone_str)


def get_phone(text):
    """
    eg:
        >>>  text = '0663-7654321, 0663-76543210, 0663-765432100, 066376543210, 0663765432100'
        >>> phones, text = get_phone(text)
        >>> phones
        >>> ['0663-7654321', '0663-76543210', '066376543210']
        >>> text
        >>> '/phone0/, /phone1/, 0663-765432100, /phone2/, 0663765432100'
    """
    phones = []
    i = 0

    while 1:
        phone = re.search(phone_str, text)
        if phone is None:
            break
        text = text.replace(phone.group(1), '/phone%s/' % str(i), 1)
        phones.append(phone.group(1))
        i += 1

    _, span_text = replace_text(text, phones, 'phone')
    return span_text, text


if __name__ == '__main__':
    text = '0663-7654321, 0663-76543210, 0663-765432100, 066376543210, 0663765432100'
    span_text, text_ = get_phone(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
