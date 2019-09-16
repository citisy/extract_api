import re
from utils import *

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
    with open('time/' + fp, 'r', encoding='utf8') as f:
        time_str += f.read().replace('\n', '|').replace(u'x', u'[0-9]').replace(u'y', u'[0-9]+').replace('!', '=')
    time_str += '|'

time_str = time_str[:-1]
time_pt = re.compile(time_str)
birth_pt = re.compile('生于/time\d/|/time\d/生[人日]|生日是?/time\d/')


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
    text, r = replace_num(text)
    times = []
    i = 0

    while 1:
        _ = time_pt.search(text)
        if _ is None:
            break
        text = text.replace(_.group(0), '/time%d/' % i, 1)
        i += 1
        times.append(_.group(0))

    for i, t in enumerate(times):  # 32号, kick off!
        if t[-1] in '号日':
            if t[:-1].isdigit():
                if int(t[:-1]) > 31:
                    text = text.replace('/time%d/' % i, times[i], 1)
                    times[i] = ''

    for i, t in enumerate(times):  # 12月, kick off!
        if t[-1] in '月':
            if t[:-1].isdigit():
                if int(t[:-1]) > 12:
                    text = text.replace('/time%d/' % i, times[i], 1)
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

    restore_num(text_, times, r)

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
        birth = birth_pt.search(text)
        if birth is None:
            break
        _ = re.search('/time(\d)/', birth.group(0))
        births.append(times[int(_.group(1))])
        text = text.replace('/time%s/' % _.group(1), '/birth%d/' % i, 1)
        i += 1

    text, _ = replace_text(text, times, 'time')
    _, span_text = replace_text(text, births, 'birth')
    return span_text, text


if __name__ == '__main__':
    text = u'我的生日是六月一号，你6月1号5点到5点半来吧，那天刚好打33号台风'
    span_text, text_, times = get_time(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
    print('--------')
    span_text, text_ = get_birth(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
