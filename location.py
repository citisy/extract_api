import jieba.posseg as pseg
from rep_tools import *

loc_str = '路|号|座|楼'


def get_loc(text):
    locs = []
    orgs = []

    # if use other segment algorithm, rewrite it!
    org_tags = ('nt', )
    loc_tags = ('ns', 'nr')
    for word, tag in pseg.cut(text):
        if tag in org_tags:
            orgs.append(word)
        if tag in loc_tags:
            locs.append(word)

    for i, _ in enumerate(locs):
        text = text.replace(_, u'/loc%s/' % str(i), 1)

    for i, _ in enumerate(orgs):
        text = text.replace(_, u'/org%s/' % str(i), 1)

    while 1:  # ns/loc + loc_str/org
        ti = re.search(u'/loc(\d+)/([\w、+-]{0,7}(?:' + loc_str + ')|/org(\d+)/)', text)
        if ti is None:
            break
        _ = ti.group(0)
        if ti.group(1):
            _ = _.replace(u'/loc%s/' % ti.group(1), locs[int(ti.group(1))])
        if ti.group(3):
            _ = _.replace(u'/org%s/' % ti.group(3), orgs[int(ti.group(3))])
        text = text.replace(ti.group(0), u'/loc%s/' % ti.group(1))
        locs[int(ti.group(1))] = _

    while 1:  # org + loc_str
        ti = re.search(u'/org(\d+)/([\w、+-]{,7}(?:' + loc_str + '))', text)
        if ti is None:
            break
        locs.append(orgs[int(ti.group(1))] + ti.group(2))
        text = text.replace(ti.group(0), u'/loc%s/' % str(len(locs)))

    while 1:  # loc + loc
        ti = re.search(u'(/loc\d+/近?){2,}', text)
        if ti is None:
            break
        s = ti.group(0)
        n = re.findall('\d+', s)
        text = text.replace(s, u'/loc%s/' % n[0], 1)
        for i, j in enumerate(n):
            s = s.replace(u'/loc%s/' % j, locs[(int(j))])
            locs[(int(j))] = ''
        locs[int(n[0])] = s

    while 1:  # loc + num
        ti = re.search(u'/loc(\d+)/([甲乙丙丁东南西北中前后左右a-zA-Z0-9、-]+米?)', text)
        if ti is None:
            break
        text = text.replace(ti.group(0), u'/loc%s/' % ti.group(1))
        if len(locs[int(ti.group(1))]) <= 4:
            continue
        else:
            locs[int(ti.group(1))] += ti.group(2)

    _, span_text = replace_text(text, locs, 'loc')
    return span_text, text


if __name__ == '__main__':
    text = u'我在江苏省南京市建邺区云龙山路88号a座3楼拐角处上班'
    span_text, text_ = get_loc(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])

