#! -*- coding:utf-8 -*-

import re
from rep_tools import *

netloc = ['com', 'cn', 'net', 'cc', 'co', 'top', 'xyz', 'wang', 'vip', 'club', 'shop', 'ltd', 'site',
          'org', 'mobi', 'online', 'store', 'ren', 'link', 'info', 'biz', 'art', 'ai', 'fm',
          u'购物', 'pro', 'tech', 'red', 'ink', 'auto', u'企业', 'love', 'work', 'fun', 'chat', 'gold',
          'plus', 'team', 'show', 'world', 'group', 'center', 'social', 'video', 'cool', 'zone',
          'today', 'city', 'company', 'live', 'fund', 'guru', 'pub', 'email', 'life', 'wiki', 'design',
          u'网店', u'中国', u'在线', u'手机', u'中文网', u'公司', u'网络', u'网址', 'name', u'我爱你', u'集团', ]

net_str = ''
for i in netloc:
    net_str += i + '|'

net_str = net_str[:-1]


def get_email(text):
    emails = []
    i = 0
    while 1:
        email = re.search(
            '[a-zA-Z0-9_.-]+'  # user name
            '@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+',  # host name
            text
        )
        if email is None:
            break
        text = text.replace(email.group(0), '/email%s/' % str(i), 1)
        emails.append(email.group(0))
        i += 1

    _, span_text = replace_text(text, emails, 'email')
    return span_text, text


def get_web(text):
    webs = []
    i = 0
    while 1:
        web = re.search(
            '(?:(?:https?|ftp|file)://)?'  # netloc
            '(?:(?:[\w-]+\.)+(?:' + net_str + ')+|(?:\d+\.){3}\d+)'  # domain, '\w' equals to '[A-Za-z0-9_]'
            '(?::\d{1,5})?'  # port
            '(?:/[\w.-]*)*'  # path
            '(?:\?[^\'",\s]*)?',
            # reauest body, it will end with ' or ' or , or blank char '\s' equals to '[ \f\n\r\t\v]'
            text
        )
        if web is None:
            break
        text = text.replace(web.group(0), '/web%s/' % str(i), 1)
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
