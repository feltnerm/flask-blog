#!/usr/bin/env python

from datetime import datetime

from flask import abort, url_for
from werkzeug import cached_property

from flaskext.mongokit import Document
from flaskext.principal import Permission, RoleNeed, UserNeed

from experientiarum.extensions import db
from experientiarum.helpers import markdown, slugify
from experientiarum.permissions import moderator, admin

def get_by_date(year=None, month=None, day=None):

    entries = db.Entry.find()
    
    matches = []
    for entry in entries:
    
        if entry.pub_date.year == year:
            matches.append(entry)
        if entry.pub_date.month == month:
            matches.append(entry)
        if entry.pub_date.day == day:
            matches.append(day)
    if matches:        
        return matches
    else:
        abort(404)

def get_by_slug(slug):
    return db.Entry.find_one_or_404({"slug":slug})

def get_by_tags(tags):
    
    matches = []
    if tags:
        for tag in tags:
            matches.append([x for x in db.Entry.find({'tags'})._get_tags() if tag in x])
        return matches
    else:
        abort(404)
        

## MODELS ##
class Entry(Document):
    ''' A single blog entry. 
    
    @todo: easy embed media (videos, images)
    @todo: add tagging
    @todo: add comments (disqus)
    '''
    
    __collection__ = 'entries'
    
    structure = {
                 'title': unicode,
                 'slug' : unicode,
                 'body' : unicode,
                 'pub_date': datetime,
                 'edit_date' : datetime,
                 'delete_date' : datetime,
                 'deleted' : bool,
                 'published' : bool,
                 'tags': unicode
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
    
    def _get_title(self):
        return self.title
    
    def _set_title(self, title):
        self.title = title.lower().strip()
        if self.slug is None:
            self.slug = slugif(title)
            
    def _get_slug(self):
        return self.slug
    
    def _set_slug(self, slug):
        if slug:
            self.slug = slugify(slug)
            
    def _get_tags(self):
        return self.tags
    
    def _set_tags(self, tags):
        
        _tags = []
        for tag in set(self.tags):
            
             _tags.append(slugify(tag))
        self.find_and_modify({'_id':self._id}, {'$set':{'tags':_tags}})
    
    @property
    def taglist(self):
        ''' Return a list of tags. '''
        if not self.tags:
            return []
        
        tags = [t.strip() for t in self.tags.split(",")]
        return [t for t in tags if t]
    
    def _url(self, external=False):
        return url_for('blog.entry', slug=self.slug, _external=external)
    
    @cached_property
    def url(self):
        return self._url()
    
    @cached_property
    def permalink(self):
        return self._url(True)
