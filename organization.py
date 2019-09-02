import re
import jieba.posseg as pseg

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
            text = text.replace(org, '/job%s/' % str(i), 1)

    return span_text, text

if __name__ == '__main__':
    text = u'我在中国人民银行和中国人民银行上班'
    span_text, text_ = get_org(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])