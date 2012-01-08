#!/usr/bin/env python

from datetime import datetime

from flask import current_app
from flaskext.mongokit import Document

## MODELS ##
class Entry(Document):
    ''' A single blog entry. 
    
    @todo: drafts (status = draft OR published)
    @todo: markdown support
    @todo: easy embed media (videos, images)
    @todo: add tagging
    @todo: add comments (disqus)'''
    
    __collection__ = 'blog_entries'
    
    structure = {
                 'title': unicode,
                 'body' : unicode,
                 'pub_date': datetime,
                 'edit_date' : datetime,
                 'delete_date' : datetime,
                 'deleted' : bool,
                 }
    required_fields = ['title', 'pub_date', 'body']
    default_values = {
                      'pub_date': datetime.utcnow,
                      'deleted' : False
                      }
    use_dot_notation = True