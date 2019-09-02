#! -*- coding: utf-8 -*-

import requests
import json
import re
from gensim.models.word2vec import Word2Vec
import numpy as np
from rep_tools import *
import codecs

cmt = []
for line in codecs.open('comment/c.txt', 'r', encoding='utf8'):
    cmt.append(line.replace('\n', '').split(' '))
sentiment_ = {-1: '消极', 1: '积极', 2: '未检测到极性', 0: '中性'}
degree = []
for line in codecs.open('comment/degree.txt', 'r', encoding='utf8'):
    degree.append(line.replace('\n', ''))
degree = degree[::-1]
loc_str = ''
for line in codecs.open('loc/loc.txt', 'r', encoding='utf8'):
    loc_str += line.replace('\n', '') + '|'
loc_str = loc_str[:-1]
wv_model = Word2Vec.load('hyapi/sg.model')
embedding_var = np.zeros((len(cmt), 128))
for k, v in enumerate(cmt):
    try:
        embedding_var[k] = wv_model[v]
    except:
        embedding_var[k] = np.random.rand(128)
emb = np.mat(embedding_var)  # use word2vec to judge the word not in cmt


class node:
    def __init__(self, data):
        self.data = data
        self.children = []


class just_a_class():
    def __init__(self, text):
        self.text = text
        self.js = self.get_js(text)

    def get_per(self):
        try:
            span_text = {}
            pers = []
            for i in self.js['items']:
                if i['ne'] == 'PER':
                    pers.append(i['item'])
            for i in pers:
                r = re.search(i, self.text)
                if r:
                    span_text[r.span()] = 'per'
            return span_text
        except KeyError:
            return []

    def get_org(self):
        try:
            span_text = {}
            orgs = []
            for i in self.js['items']:
                if i['ne'] == 'ORG':
                    orgs.append(i['item'])
            for i in orgs:
                r = re.search(i, self.text)
                if r:
                    span_text[r.span()] = 'org'
            return span_text
        except KeyError:
            return []

    def get_loc(self):
        try:
            locs = []
            orgs = []
            for i in self.js['items']:
                if i['ne'] == 'ORG':
                    orgs.append(i['item'])
                if i['ne'] == 'LOC':
                    locs.append(i['item'])
        except KeyError:
            return []
        text = self.text
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
        text, span_text = replace_text(text, locs, 'loc')
        return span_text

    def get_js(self, text):
        sess = requests.session()
        ip = '10143735'
        apikey = 'LHPOEDOgGOEiVpPgOIanepaE'
        sk = '8DyoLlwmjRMIYgCM4kSxdYRT6N1MVGNG'
        keyurl = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=LHPOEDOgGOEiVpPgOIanepaE&client_secret=8DyoLlwmjRMIYgCM4kSxdYRT6N1MVGNG'
        html = sess.get(keyurl)
        js = json.loads(html.text)
        ner_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer?charset=UTF-8&access_token=%s' % js['access_token']
        rejs = {
            'text': text
        }
        header = {
            'Content-Type': 'json'
        }
        html = sess.post(url=ner_url, json=rejs, headers=header)
        js = json.loads(html.text)
        return js

    def get_comment(self):
        # -------- extract ----------
        # get word is conformed to the rules
        # return sl -> 3-D list, 0d -> sens, 1d -> words, 2d -> word's attributes
        try:
            self.js['items']
        except KeyError:
            return []
        root = self.make_tree()
        pn = root
        s = []  # [depth, word, pos]
        sl = []  # [(sen1)[[depth1, word1, pos1], ...], [[]], ...]
        textt = ''
        for i in self.js['items']:
            # print(i['item'], i['ne'], i['pos'])
            textt += '%s/%s ' % (i['item'], i['pos'])
            if i['pos'] in 'fmst':  # pos in 'fmst' is stopword
                continue
            if i['pos'] in 'uq':  # specially, let word '的' be the stopword
                if i['item'] != u'的':
                    continue
            if i['pos'] == 'an':  # let the 'an' be the 'a'
                i['pos'] = 'a'
            if i['item'] in [u'好评', u'差评', u'标准', u'棒棒']:  # specially, let these words be the 'a'
                i['pos'] = 'a'
            for child in pn.children:  # child.data -> [pos, depth]
                if child.data[0] == 'o':
                    if child.children > 0:
                        sl.append([])
                        flag = 0
                        posl = ''
                        for _ in s:
                            if _[0] >= child.children:
                                flag = 1
                            if flag == 1:
                                if len(posl) != 0 and _[2] == 'n' and posl[-1] != 'n' and 'n' in posl:  # nana -> na, na
                                    sl.append([])
                                    posl = ''
                                if len(posl) != 0 and _[2] == 'a' and posl[
                                    -1] != 'a' and 'a' in posl:  # aana -> aan, na
                                    sl.append([])
                                    posl = ''
                                sl[-1].append(_)
                                posl += _[2]
                    pn = root
                    s = []
                    for _ in pn.children:
                        if _.data[0] in i['pos']:
                            s.append([_.data[1], i['item'], _.data[0]])
                            pn = _
                            break
                elif child.data[0] in i['pos']:
                    s.append([child.data[1], i['item'], child.data[0]])
                    pn = child
                    break
            if i['pos'] == 'w' and i['item'] not in u'，、： ':
                sl.append([[-1, '', 'n']])
        # -------- extract ----------

        # -------- select -----------
        # select sens conformed to the rules from sl, then add the sentiment
        # return sl -> list, [str0, str1]
        d = {}
        for i, s in enumerate(sl):
            d[i] = {'n': '', 'a': '', 'v': '', 'p': 2}
            if len(s) <= 1:
                continue
            for s_ in s:  # s_ -> [depth, word, pos]
                if s_[2] == 'n':
                    d[i]['n'] += s_[1].replace(u'　', '').replace('\r', '').replace('\n', '')
                elif s_[2] in 'adu':
                    for _ in degree:
                        s_[1] = s_[1].replace(_, '')
                    if s_[1] == '':
                        continue
                    if s_[2] in 'da':
                        d[i]['a'] += s_[1]
                    flag = 0
                    for _ in cmt:
                        if s_[1] == _[0]:
                            if d[i]['p'] == 2:
                                d[i]['p'] = 1
                            d[i]['p'] *= int(_[1])
                            flag = 1
                            break
                    if flag == 0:  # use word2vec to judge the word not in cmt
                        try:
                            wv = wv_model[s_[1]]
                            wv = np.mat(wv)
                            x = np.matmul(wv, emb.T) / (np.linalg.norm(wv) * np.linalg.norm(emb))
                            argmi = np.argmax(x)
                            if d[i]['p'] == 2:
                                d[i]['p'] = 1
                            d[i]['p'] *= int(cmt[argmi][1])
                        except:
                            pass
                elif s_[2] == 'v':
                    d[i]['v'] += s_[1]
            if d[i]['n'] == '':
                if d[i]['v'] != '':
                    d[i]['n'] = d[i]['v']
                else:
                    try:
                        d[i]['n'] = d[i - 1]['n']
                    except:
                        pass
        comments = []
        for v in d.values():
            if v['n'] == '' or v['a'] == '':
                continue
            comments.append({'主体': v['n'], '属性': v['a'], '极性': sentiment_[v['p']]})
        # -------- select -----------

        # -------- add --------------
        # specially, add some cmt to sl
        posl = ''
        segl = []
        for i in self.js['items']:  # if 'waw', add 主体 -> '感觉', eg: 房间很大，很棒。-> 房间很大，感觉很棒。
            if i['pos'] != 'w':
                posl += i['pos']
                segl.append(i['item'])

            elif i['item'] in u'，。！：？；、':  # some punctuation cant' cut the seg, like '《》（）'
                """
                can't access example: wanw, wdw, ww
                eg: 
                    房间很大，很棒。 -> pos tags -> ndawdaw
                    posl -> da
                    segl -> ['很', '棒']
                """
                if set(list(posl)).issubset(set(['d', 'a', 'u'])) and set('a').issubset(list(posl)) and len(
                        set(list(posl))) != 0:
                    p = 2
                    for k, se in enumerate(segl):
                        for _ in degree:  # remove degree words
                            se = se.replace(_, '')
                        if se == '':
                            continue
                        segl[k] = se
                        flag = 0
                        for _ in cmt:  # in comment words
                            if se == _[0]:
                                if p == 2:
                                    p = 1
                                p *= int(_[1])
                                flag = 1
                                break
                        if flag == 0:  # if not in comment words, use word2vec to judge the word
                            try:
                                wv = wv_model[se]
                                wv = np.mat(wv)
                                x = np.matmul(wv, emb.T) / (np.linalg.norm(wv) * np.linalg.norm(emb))
                                argmi = np.argmax(x)
                                if p == 2:
                                    p = 1
                                p *= int(cmt[argmi][1])
                            except:
                                pass
                    comments.append({'主体': '感觉', '属性': ''.join(segl), '极性': sentiment_[p]})
                posl = ''
                segl = []
        # -------- add --------------

        return comments

    def make_tree(self):
        root = node(None)
        n = node(['n', 1])
        nv, na, nd, nn, no = node(['v', 2]), node(['a', 2]), node(['d', 2]), n, node(['o', 2])
        a, d, v, p, o = node(['a', 1]), node(['d', 1]), node(['v', 1]), node(['p', 1]), node(['o', 1])
        au, aa, ao = node(['u', 2]), a, node(['o', 2])
        da, dd, do = a, d, node(['o', 2])
        vv, vu, vo = v, node(['u', 2]), node(['o', 2])
        pp, pn, po = p, node(['n', 2]), node(['o', 2])
        nva, nvd, nvv, nvo = na, nd, nv, node(['o', 3])
        nan, naa, nau, nav, nao = node(['n', 3]), na, node(['u', 3]), node(['v', 3]), node(['o', 3])
        nda, ndd, ndo = na, nd, node(['o', 3])
        auu, aun, auo = au, n, node(['o', 3])
        vuu, vun, vuo = vu, node(['n', 3]), node(['o', 3])
        pnn, pno = pn, node(['o', 3])
        nann, nana, nano = nan, na, node(['o', 4])
        naun, nauu, nauo = nan, nau, node(['o', 4])
        navv, navo = nav, node(['o', 4])
        vunn, vund, vuna, vuno = vun, node(['d', 4]), node(['a', 4]), node(['o', 4])
        vundd, vunda = vund, vuna
        vunaa, vunao = vuna, node(['o', 5])
        root.children = [n, a, d, v, p, o]
        n.children = [nn, nv, na, nd, no]
        a.children = [aa, au, ao]
        d.children = [da, dd, do]
        v.children = [vv, vu, vo]
        p.children = [pp, pn, po]
        o.children = 0
        nv.children = [nvv, nva, nvd, nvo]
        na.children = [nan, naa, nau, nav, nao]
        nd.children = [nda, ndd, ndo]
        no.children = 1
        au.children = [auu, aun, auo]
        ao.children = 0
        do.children = 0
        vu.children = [vuu, vun, vuo]
        vo.children = 0
        pn.children = [pnn, pno]
        po.children = 0
        nvo.children = 0
        nan.children = [nann, nana, nano]
        nau.children = [naun, nauu, nauo]
        nav.children = [navv, navo]
        nao.children = 1
        ndo.children = 0
        auo.children = 0
        vun.children = [vunn, vuna, vund, vuno]
        vuo.children = 0
        pno.children = 0
        nano.children = 2
        navo.children = 0
        nauo.children = 1
        vund.children = [vunda, vundd]
        vuna.children = [vunaa, vunao]
        vuno.children = 0
        vunao.children = 0
        return root


if __name__ == '__main__':
    # text = '北京的风景很美环境不错，很棒'
    text = u'李梅梅在广州黄埔花园买了部非常不智能的手机，是三星品牌的'
    # text = '风景不漂亮'
    c = just_a_class(text)
    span_text = c.get_per()
    print(span_text)
    span_text = c.get_org()
    print(span_text)
    span_text = c.get_loc()
    print(span_text)
    comments = c.get_comment()
    print(comments)
