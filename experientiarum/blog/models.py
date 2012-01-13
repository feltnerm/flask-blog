#!/usr/bin/env python

from datetime import datetime

from flaskext.mongokit import Document

## MODELS ##
class Entry(Document):
    ''' A single blog entry. 
    
    @todo: drafts (status = draft OR published)
    @todo: markdown support
    @todo: easy embed media (videos, images)
    @todo: add tagging
    @todo: add comments (disqus)
    '''
    
    __collection__ = 'blog_entries'
    
    structure = {
                 'title': unicode,
                 'slug' : unicode,
                 'body' : unicode,
                 'pub_date': datetime,
                 'edit_date' : datetime,
                 'delete_date' : datetime,
                 'deleted' : bool,
                 'published' : bool,
                 'tags': [unicode]
                 }
    required_fields = ['title']
    default_values = {
                      'pub_date': datetime.utcnow(),
                      'deleted' : False
                      }
    indexes = [
               {'fields': 'slug',},
               {'fields': 'deleted'},
               {'fields': 'pub_date'}
               ]
    use_dot_notation = True
