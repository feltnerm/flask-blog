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

    dt = datetime(year, month, day)
    return db.Entry.find({'pub_date':dt})

def get_by_slug(slug):
    return db.Entry.find_one_or_404({"slug":slug})

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
        
        self.tags = tags
        
        if self.id:
            # ensure existing tag references
            # are removed
            pass
            
        for tag in set(self.taglist):
            # set tags
            
            # slug = slugify(taglist)
            # tag = db.Tag.find_one({"slug":slug})
            # if tag is None:
            #    # create a new tag
            #    tag = db.Tag()
            #    tag.slug = slug
            #
            # tag.posts.append(self)
            # tag.save()
            pass
    
    @property
    def taglist(self):
        ''' Return a list of tags. '''
        if not self.tags:
            return []
        
        tags = [t.strip() for t in self.tags.split(",")]
        return [t for t in tags if t]
    
    def _url(self, external=False):
        #return url_for('blog.entry', external=external)
        pass
    
    @cached_property
    def url(self):
        return self._url()
    
    @cached_property
    def permalink(self):
        return self._url(True)
