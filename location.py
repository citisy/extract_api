import jieba.posseg as pseg
from utils import *

with open('loc/loc.txt', 'r', encoding='utf8') as f:
    loc_str = f.read().replace('\n', '|')


def get_loc(text):
    locs = []
    orgs = []

    # if use other segment algorithm, rewrite it!
    org_tags = ('nt',)
    loc_tags = ('ns', 'nr')
    for word, tag in pseg.cut(text):
        if tag in org_tags:
            orgs.append(word)
        if tag in loc_tags:
            locs.append(word)

    for i, loc in enumerate(locs):
        text = text.replace(loc, u'/loc%d/' % i, 1)

    for i, org in enumerate(orgs):
        text = text.replace(org, u'/org%d/' % i, 1)

    while 1:  # ns/loc + loc_str/org
        ti = re.search(u'/loc(\d+)/([\w、+-]{,7}(?:' + loc_str + ')|/org(\d+)/)', text)
        if ti is None:
            break
        _ = ti.group(0)

        if ti.group(1):
            _ = _.replace(u'/loc%s/' % ti.group(1), locs[int(ti.group(1))], 1)
        if ti.group(3):
            _ = _.replace(u'/org%s/' % ti.group(3), orgs[int(ti.group(3))], 1)

        text = text.replace(ti.group(0), u'/loc%s/' % ti.group(1), 1)
        locs[int(ti.group(1))] = _

    while 1:  # org + loc_str
        ti = re.search(u'/org(\d+)/([\w、+-]{,7}(?:' + loc_str + '))', text)
        if ti is None:
            break
        locs.append(orgs[int(ti.group(1))] + ti.group(2))
        text = text.replace(ti.group(0), u'/loc%d/' % len(locs), 1)

    while 1:  # loc + loc
        ti = re.search(u'(/loc\d+/近?){2,}', text)
        if ti is None:
            break
        s = ti.group(0)
        n = re.findall('\d+', s)
        text = text.replace(s, u'/loc%s/' % n[0], 1)

        for i, j in enumerate(n):
            s = s.replace(u'/loc%s/' % j, locs[(int(j))], 1)
            locs[(int(j))] = ''

        locs[int(n[0])] = s

    while 1:  # loc + num
        ti = re.search(u'/loc(\d+)/([甲乙丙丁东南西北前后左右里外中内旁上下a-zA-Z0-9、-]+米?)', text)
        if ti is None:
            break
        text = text.replace(ti.group(0), u'/loc%s/' % ti.group(1), 1)

        if len(locs[int(ti.group(1))]) <= 4:  # if the string is too short, it isn't a location string probability
            continue
        else:
            locs[int(ti.group(1))] += ti.group(2)

    _, span_text = replace_text(text, locs, 'loc')
    return span_text, text


if __name__ == '__main__':
    text = '公司地址：南京市建邺区云龙山路88号烽火科技大厦，邮编210019'
    span_text, text_ = get_loc(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
