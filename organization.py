import re
import jieba.posseg as pseg
from utils import *


def get_org(text):
    words = pseg.cut(text)

    span_text = {}
    orgs = []
    for word, tag in words:
        if tag == 'nt':
            orgs.append(word)

    for i, org in enumerate(orgs):
        r = re.search(org, text)
        if r:
            span_text[r.span()] = 'org'
            text = text.replace(org, '/org%d/' % i, 1)

    _, span_text = replace_text(text, orgs, 'org')
    return span_text, text


if __name__ == '__main__':
    text = u'中国人民银行，简称央行，是中华人民共和国的中央银行，中华人民共和国国务院组成部门'
    span_text, text_ = get_org(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
