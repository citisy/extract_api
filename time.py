#! -*- coding:utf-8 -*-

import re
import codecs
from rep_tools import *


fps = [
    'synonym.txt',
    'time.txt',
    'day.txt',
    'month.txt',
    'year.txt',
    'festival.txt'
]

time_str = ''
for fp in fps:
    for line in codecs.open('time/' + fp, 'r', encoding='utf8'):
        i = line.lstrip('\ufeff').rstrip('\n').strip().split('=')
        s = i[0].replace(u'x', u'[0-9]').replace(u'y', u'[0-9]+').replace('!', '=')
        time_str += s + '|'

time_str = time_str[:-1]
time_str = re.compile(time_str)


def get_time(text):
    """
    eg:
        >>> text = u'我的生日是六月一号，你6月1号5点到5点半来吧'
        >>> times, text = get_time(text)
        >>> times
        >>> [u'6月1号', u'6月1号5点到5点半', '', '']
        >>> text
        >>> u'我的生日是/time0/，你/time1/来吧'
    """
    text_ = text
    text = text.replace(
        u'一', '1').replace(u'二', '2').replace(u'三', '3').replace(u'四', '4').replace(u'五', '5').replace(
        u'六', '6').replace(u'七', '7').replace(u'八', '8').replace(u'九', '9').replace(u'两', '2').replace(u'零', '0')

    text = re.sub(u'([十百千万亿]?(?:\d+(?:[\.]\d+)?[十百千万亿]*)+\d*)+|[十百千万亿]', replace_num, text)
    times = []
    i = 0

    while 1:
        _ = re.search(time_str, text)
        if _ is None:
            break
        text = text.replace(_.group(0), '/time%s/' % str(i), 1)
        i += 1
        times.append(_.group(0))

    for i, t in enumerate(times):   # 32号, kick off!
        if u'号' == t[-1]:
            if t[:-1].isdigit():
                if int(t[:-1]) > 31:
                    text = text.replace('/time%s/' % str(i), times[i], 1)
                    times[i] = ''

    while 1:
        """
        text: /time0/到/time1/, /time2/到/time3/ -> /time0/, /time2/
        times: [time0, 1, 2, 3] -> [time0, '', 2, '']
        """
        ti = re.search(u'([到至]?/time\d+/){2,}', text)
        if ti is None:
            break
        s = ti.group(0)
        n = re.findall('\d+', s)
        text = text.replace(s, '/time%s/' % n[0], 1)
        for i, j in enumerate(n):
            s = s.replace('/time%s/' % j, times[(int(j))])
            times[(int(j))] = ''
        times[int(n[0])] = s

    x = 0
    for i in r:
        for j in range(x, len(times)):
            if i[1] in times[j]:
                times[j] = times[j].replace(i[1], text_[i[0][0]:i[0][1]], 1)
                x = j
                break

    _, span_text = replace_text(text, times, 'time')
    return span_text, text, times


def get_birth(text):
    """
    use it behind to get_time
    """
    _, text, times = get_time(text)
    births = []
    i = 0

    while 1:
        birth = re.search(
            u'生于/time\d/|/time\d/生[人日]|生日是?/time\d/',
            text
        )
        if birth is None:
            break
        _ = re.search('/time(\d)/', birth.group(0))
        births.append(times[int(_.group(1))])
        text = text.replace('/time%s/' % _.group(1), '/birth%s/' % str(i), 1)
        i += 1

    text, _ = replace_text(text, times, 'time')
    _, span_text = replace_text(text, births, 'birth')
    return span_text, text


r = []
def replace_num(text_):
    """
    step:
        * replace chinese num, eg: 这次的金钱是十一亿二千三十四万五千六百零七块 -> 这次的金钱是十1亿2千3十4万5千6百07点8块
        * find num str, eg: 这次的金钱是十一亿二千三十四万五千六百零七块 -> 十1亿2千3十4万5千6百07点8
        * replace u'百千万亿u', eg: 十1亿2千314万5千6百07 -> 11023145607.8
    ---------
    eg:
        >>> text = u'十一亿二千三十四万五千六百零七点八'
        >>> replace_num(text)
        >>> 11023145607.8
    """
    span = text_.span()
    text = text_.group()
    num = 0
    shi, bai, qian, wan, yi = [1] * 5
    d = 1
    for i in text[::-1]:
        try:  # when i is int type
            num += int(i) * d * shi * bai * qian * wan * yi
            d *= 10
        except:  # when type is str type, eg: 十百千万亿
            if i == u'十':
                shi *= 10
            if i == u'百':
                shi = 1
                bai *= 100
            if i == u'千':
                shi, bai = [1] * 2
                qian *= 1000
            if i == u'万':
                shi, bai, qian = [1] * 3
                wan *= int(1e4)
            if i == u'亿':
                shi, bai, qian, wan = [1] * 4
                yi *= int(1e8)
            if i == '.' or i == u'点':
                if num < d:
                    num /= d
                else:
                    num //= d
            d = 1

    if d == 1:  # when d = 1, meaning that the last operation didnu't be added, eg: 十1亿, operation u'十' will be ignored
        num += 1 * d * shi * bai * qian * wan * yi

    r.append([span, str(num)])
    return str(num)


if __name__ == '__main__':
    text = u'我的生日是六月一号，你6月1号5点到5点半来吧'
    span_text, text_, times = get_time(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
    print('--------')
    span_text, text_ = get_birth(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
