#!/usr/bin/env python

import re
import markdown
import urlparse
import functools
import hashlib
import socket, struct

from datetime import datetime

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from flask import current_app, g


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
_pre_re = re.compile(r'<pre (?=l=[\'"]?\w+[\'"]?).*?>(?P<code>[\w\W]+?)</pre>')
_lang_re = re.compile(r'l=[\'"]?(?P<lang>\w+)[\'"]?')

''' Turns markdown into unicode HTML. '''
md = functools.partial(markdown.markdown,
                             safe_mode='remove',
                             output_format="html")

def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug. From http://flask.pocoo.org/snippets/5/"""
    result = []
    for word in _punct_re.split(text.lower()):
        #word = word.encode('translit/long')
        if word:
            result.append(word)
    return unicode(delim.join(result))

def domain(url):
    """
    Returns the domain of a URL e.g. http://reddit.com/ > reddit.com
    """
    rv = urlparse.urlparse(url).netloc
    if rv.startswith("www."):
        rv = rv[4:]
    return rv

def gistcode(content):
    result = list(set(re.findall(r"(<a[^<>]*>\s*(https://gist.github.com/\d+)\s*</a>)", content)))
    for i,link in result:
        content = content.replace(i, '%s <script src="%s.js"></script>' % (i, link))
    return content

def code_highlight(value):
    f_list = _pre_re.findall(value)

    if f_list:
        s_list = _pre_re.split(value)

        for code_block in _pre_re.finditer(value):

            lang = _lang_re.search(code_block.group()).group('lang')
            code = code_block.group('code')

            index = s_list.index(code)
            s_list[index] = code2html(code, lang)

        return u''.join(s_list)

    return value
    
def code2html(code, lang):
    lexer = get_lexer_by_name(lang, stripall=True)
    formatter = HtmlFormatter()
    return highlight(code, lexer, formatter)

def ip2long(ip):
    return struct.unpack("!I",socket.inet_aton(ip))[0]

def long2ip(num):
    return socket.inet_ntoa(struct.pack("!I",num))
    