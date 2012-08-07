#!/usr/bin/env python

import urllib2
from datetime import datetime

from flask import abort, url_for
from werkzeug import cached_property

from flask.ext.mongokit import Document

from apps.extensions import db

#@TODO
def get_by_date(year=None, month=None, day=None):
    """ Retrieve one or more entries based on the year, month, and/or day. """

    entries = db.Entry.find({'deleted':False, 'published': True})
    if year is None and month is None and day is None:
        return entries
    
    matches = []
    for entry in entries:
    
        if year == entry.pub_date.year and month == entry.pub_date.month and day == entry.pub_date.day:
            matches.append(entry)
        
        elif day is None:
            if entry.pub_date.year == year and entry.pub_date.month == month:
                matches.append(entry)

            elif month is None:
                if entry.pub_date.year == year:
                    matches.append(entry)

    return matches

def get_by_slug(slug, published = True, deleted = False):
    """ Retrieve one entry or return a 404 error. """

    return db.Entry.find_one_or_404({'slug':slug, 'published': published
                                     ,'deleted': deleted})

#@TODO
def get_by_tags(tags):
   
    result = []
    for r in db.Entry.find({"deleted":False, "published":True}).sort('pub_date',-1):
        for tag in tags.split("+"):
            if tag in r.tags:
                if not r in result:
                    result.append(r)
    return result


#@TODO
def get_by_labels(labels):
    """ Retrieve all entries whose label(s) match labels.
    Labels could be one string or a list of them.
    """

    matches = []
    if labels:
        for label in labels:
            matches.append([x for x in db.Entry.find({'labels'})._get_labels() if label in x])
        return matches
    else:
        abort(404)

## MODELS ##
class Entry(Document):
    """ A single blog entry. 
    ## Attributes
        title       -- title of the Entry
        slug        -- shortened version of the Entry title
        body        -- the actual text of the Entry
        abstract    -- short teaser
        tags        -- a list of tags pertaining to this Entry
        published   -- whether or not the post has been marked as 'published'
        pub_date    -- the date the Entry was originally published
        edit_date   -- the date of the most previous edit
        deleted     -- whether or not the post has been marked as 'deleted'
        delete_date -- the date of deletion (if applicable)
    
    """
    
    __collection__ = 'entries'
    use_dot_notation = True

    structure = {
                 'title': unicode,
                 'slug' : unicode,
                 'body' : unicode,
                 'abstract': unicode,
                 'tags': list,
                 'published' : bool,
                 'pub_date': datetime,
                 'edit_date' : datetime,
                 'deleted' : bool,
                 'delete_date' : datetime
                 }

    required_fields = ['title', 'slug', 'body', 'pub_date', 'deleted']
    default_values = {
                      'pub_date': datetime.utcnow(),
                      'published': True,
                      'deleted' : False
                      }
    #@TODO
    # indexes = [
    #            {'fields': 'slug',},
    #            {'fields': 'deleted'},
    #            {'fields': 'pub_date'},
    #            {'fields': ['title', 'body', 'pub_date', 'edit_date']}
    #            {'fields': 'labels'}
    #            ]

    def set_tags(self, tags):
        """ take a comma-delimited list of tags and append them to the 
        model's taglist, if not already in the taglist.
        """
        self.tags = []
        for tag in [t.strip() for t in tags.split(',')]:
            if not tag in self.tags:
                self.tags.append(tag)

    def get_tags(self):
        if not self.tags:
            return ''
        return ', '.join(self.tags)

    @property
    def taglist(self):
        if self.tags is None:
            return []

        return [t.strip() for t in self.tags.split(",")]

    def _url(self, external=False):
        return url_for('blog.entry', slug=self.slug, _external = external)
    
    @cached_property
    def url(self):
        return self._url()

    @cached_property
    def permalink(self):
        return self._url(True)
