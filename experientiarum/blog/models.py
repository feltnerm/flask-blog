#!/usr/bin/env python

from datetime import datetime

from flaskext.mongokit import MongoKit, Document, Set

## MODELS ##
class Entry(Document):
    ''' A single blog entry. 
    
    @todo: drafts (status = draft OR published)
    @todo: markdown support
    @todo: easy embed media (videos, images)
    @todo: add tagging
    @todo: add comments (disqus)'''
    
    __collection__ = 'entries'
    
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
                      'published' : False,
                      'deleted' : False
                      }
    use_dot_notation = True
    
## DATABASE ##