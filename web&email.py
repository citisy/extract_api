#! -*- coding:utf-8 -*-
"""if you want to extract email and web at the same time,
you must extract the email first than web,
'cause the web contains the email
"""

import re
from utils import *

with open('web/netloc.txt', 'r', encoding='utf8') as f:
    net_str = f.read().replace('\n', '|')

email_pt = re.compile('[a-zA-Z0-9_.-]+'  # user name
                      '@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+'  # host name
                      )

web_pt = re.compile('(?:(?:https?|ftp|file)://)?'  # netloc
                    '(?:(?:[\w-]+\.)+(?:' + net_str + ')+|(?:\d+\.){3}\d+)'  # domain, '\w' equals to '[A-Za-z0-9_]'
                    '(?::\d{1,5})?'  # port
                    '(?:/[\w.-]*)*'  # path
                    '(?:\?[^\'",\s]*)?'    # reauest body
                    )


def get_email(text):
    emails = []
    i = 0
    while 1:
        email = email_pt.search(text)
        if email is None:
            break
        text = text.replace(email.group(0), '/email%d/' % i, 1)
        emails.append(email.group(0))
        i += 1

    _, span_text = replace_text(text, emails, 'email')
    return span_text, text


def get_web(text):
    webs = []
    i = 0
    while 1:
        web = web_pt.search(text)
        if web is None:
            break
        text = text.replace(web.group(0), '/web%d/' % i, 1)
        webs.append(web.group(0))
        i += 1

    _, span_text = replace_text(text, webs, 'web')
    return span_text, text


if __name__ == '__main__':
    text = 'https://news.sina.com.cn/n?d=1, 111@qq.com'
    span_text, text_ = get_email(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])

    span_text, text_ = get_web(text_)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
