#!/usr/bin/env python

import re

from datetime import datetime

from flask import url_for
from werkzeug.routing import BuildError

from pymongo.son_manipulator import ObjectId


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def format_date(date):
    ''' @todo: convert mongodb datetime objects to a human readable thing '''
    return date.strftime('%b %d, %Y')

def format_datetime(datetime):
    ''' @todo: convert mongodb datetime objects to a human readable thing. '''
    return datetime.strftime('%I:%M.%S%p %A %B %d, %Y')

def gistcode(content):
    ''' When a gistcode is embedded in the document, render it '''
    result = list(set(re.findall(r"(<a[^<>]*>\s*(https://gist.github.com/\d+)\s*<a/>", content)))
    for i, link in result:
        content = content.replace(i, '%s <script src="%s.js"></script>' % (i, link))
    return content

def request_wants_json(request):
    """ only accept json if the quality of the json is greater than
    the quality of the text/html because text/html is preferred to support
    browsers that accept on */*
    """

    best = request.accept_mimetypes.best_match(['application/json','text/html'])
    return best == 'application/json' and \
            request.accept_mimetypes[best] > request.accept_mimetypes['text/html']

def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug. From http://flask.pocoo.org/snippets/5/"""
    result = []
    for word in _punct_re.split(text.lower()):
        #word = word.encode('translit/long')
        if word:
            result.append(word)
    return unicode(delim.join(result))

def to_oid(sid):
    return ObjectId(sid)

def timesince(dt, past_="ago", future_="from now", default="just now"):
    """
    Returns string representing "time since"
    or "time until" e.g.
    3 days ago, 5 hours from now etc.
    """

    now = datetime.utcnow()
    if now > dt:
        diff = now - dt
        dt_is_past = True
    else:
        diff = dt - now
        dt_is_past = False

    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:

        if period:
            return "%d %s %s" % (period, \
                singular if period == 1 else plural, \
                past_ if dt_is_past else future_)

    return default

def permalink(function):
    def inner(*args, **kwargs):
        endpoint, values = function(*args, **kwargs)
        try:
            return url_for(endpoint, **values)
        except BuildError:
            return
    return inner
