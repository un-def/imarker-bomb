#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from string import ascii_lowercase
from flup.server.fcgi import WSGIServer

def app(environ, start_response):
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    content = []
    if environ['PATH_INFO'] == '/':
        status = '302 Found'
        url = 'http://'
        if environ.get('HTTP_HOST'):
            url += environ['HTTP_HOST']
        else:
            url += environ['SERVER_NAME']
            if environ['SERVER_PORT'] != '80':
                url += ':' + environ['SERVER_PORT']
        url += '/' + ''.join(random.choice(ascii_lowercase) for n in range(10))
        headers.append(('Location', url))
    else:
        status = '200 OK'
        user_agent = environ.get('HTTP_USER_AGENT', '[header is missing]')
        if user_agent == 'WebIndex':
            headers = [('Content-type', 'text/html; charset=utf-8'), ('Content-Encoding', 'gzip')]
            bomb = open('bomb-html-char-X-1k.html.gz', 'rb')
            content = iter(lambda: bomb.read(8192), '')
        else:
            content.append("Your User-Agent: {0}\n\nTry 'WebIndex' instead.\n".format(user_agent))
    start_response(status, headers)
    return content

WSGIServer(app).run()
