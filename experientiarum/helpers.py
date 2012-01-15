#!/usr/bin/env python

import re
from markdown import markdown
import functools

from datetime import datetime

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def markup(text):
    ''' Converts a text (with markup + code) to HTML '''
    return markdown(text, ['codehilite'])
    

def format_date(date):
    ''' @todo: convert mongodb datetime objects to a human readable thing '''
    return date.strftime('%A %B %d, %Y')

def format_datetime(datetime):
    ''' @todo: convert mongodb datetime objects to a human readable thing. '''
    return datetime.strftime('%I:%M.%S%p %A %B %d, %Y')

def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug. From http://flask.pocoo.org/snippets/5/"""
    result = []
    for word in _punct_re.split(text.lower()):
        #word = word.encode('translit/long')
        if word:
            result.append(word)
    return unicode(delim.join(result))
    
