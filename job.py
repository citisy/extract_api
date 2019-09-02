#! -*- coding:utf-8 -*-

import re
import codecs
from rep_tools import *


job_str = ''
for line in codecs.open('job/job.txt', 'r', encoding='utf8'):
    job_str += line.replace('\n', '') + '|'

job_str = job_str[:-1]


def get_job(text):
    jobs = []
    i = 0

    while 1:
        job = re.search(
            job_str,
            text
        )
        if job is None:
            break
        text = text.replace(job.group(0), '/job%s/' % str(i), 1)
        jobs.append(job.group(0))
        i += 1

    _, span_text = replace_text(text, jobs, 'job')
    return span_text, text


if __name__ == '__main__':
    text = u'可以到求职网找保姆哦'
    span_text, text_ = get_job(text)
    print(span_text)
    for k, v in span_text.items():
        print(k, text[k[0]:k[1]])
