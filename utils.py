#! -*- coding: utf-8 -*-

import re


def replace_text(text, li, s):
    """
    restore the text and give the right span_text
    eg:
        input: text=我有/money0/, li=[110元], s=money
        return: text=我有110元, span_text=(3, 6)
    """
    span_text = {}
    for i, l in enumerate(li):
        if l == '':
            continue
        _ = re.search('/%s%d/' % (s, i), text)
        if _:
            text = text.replace('/%s%d/' % (s, i), l, 1)
            span = _.span()
            span_text[(span[0], span[0] + len(l))] = s
    return text, span_text


def replace_num(text, flag='other'):
    r = []

    def chinese2simple(text_):
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

    text = text.replace(
        u'壹', '1').replace(u'贰', '2').replace(u'叁', '3').replace(u'肆', '4').replace(u'伍', '5').replace(
        u'陆', '6').replace(u'柒', '7').replace(u'捌', '8').replace(u'玖', '9').replace(u'拾', u'十').replace(
        u'佰', u'百').replace(u'仟', u'千').replace(
        u'一', '1').replace(u'二', '2').replace(u'三', '3').replace(u'四', '4').replace(u'五', '5').replace(
        u'六', '6').replace(u'七', '7').replace(u'八', '8').replace(u'九', '9').replace(u'两', '2').replace(u'零', '0')
    if flag == 'time':
        text = re.sub(u'([十百千万亿]?(?:\d+(?:[\.]\d+)?[十百千万亿]*)+\d*)+|[十百千万亿]', chinese2simple, text)
    else:
        text = re.sub(u'([十百千万亿]?(?:\d+(?:[\.点]\d+)?[十百千万亿]*)+\d*)+|[十百千万亿]', chinese2simple, text)
    return text, r


def restore_num(text, obj, r):
    x = 0
    for span, num in r:
        for j in range(x, len(obj)):
            if num in obj[j]:
                obj[j] = obj[j].replace(num, text[span[0]:span[1]], 1)
                x = j
                break
