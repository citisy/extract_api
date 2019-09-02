from weburl import get_web

with open('apk_url.txt', 'w', encoding='utf8') as f:
    for line in open('content.txt', 'r', encoding='utf8'):
        span, text = get_web(line)
        for k, v in span.items():
            f.write(line[k[0]:k[1]] + '\n')

