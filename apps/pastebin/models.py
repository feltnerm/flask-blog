#!/usr/bin/env python

from datetime import datetime

from flask import abort, url_for
from werkzeug import cached_property

from flaskext.mongokit import Document

from experientiarum.extensions import db

def get_by_date(year=None, month=None, day=None):
    """ Get all pastes pertaining to a certain year, month, and/or day """
    pass

def get_by_labels(labels):
    """ All pastes with a label in the list of labels passed. """
    pass

def get_by_slug(slug, deleted=False):
    """ Get a paste by looking up its slug. """
    return db.Paste.find_one_or_404({'slug': slug, 'deleted': deleted})

def get_by_language(language, deleted=False):
    """ Get a paste by the type of code it is. """
    return db.Paste.find({'language': language, 'deleted': deleted}).sort('pub_date', -1)

class Paste(Document):
    """ A single paste of code. 
    ## Attributes
        title           -- title of the Paste
        slug            -- shortened version of the Paste title
        body            -- the code the paste refers to
        explanation     -- a quick explanation of the code
        language        -- they language the Paste is predominately in
        labels          -- a list of labels pertaining to the Paste
        source          -- citations (if needed)
        documentation   -- the generated documentation for the paste
        pub_date        -- date the Paste was published
        edit_date       -- the date of the most previous edit
        deleted         -- whether or not the Paste has been marked 'deleted'
        delete_date     -- the date of deletion (if applicable)
    """

    __collection__ = 'pastes'
    use_dot_notation = True

    structure = {
                 'title': unicode,
                 'slug': unicode,
                 'body': unicode,
                 'explanation': unicode,
                 'language': unicode,
                 'labels': list,
                 'source': unicode,
                 'documentation': unicode,
                 'pub_date': datetime,
                 'edit_date': datetime,
                 'delete_date': datetime,
                 'deleted' : bool
                 }

    required_values = ['title', 'slug', 'body', 'language', 'labels']
    default_values = {
            'pub_date': datetime.utcnow(),
            'deleted': False,
            }
    # indexes = [
    #         {'fields': 'slug',}
    #         {'fields': 'deleted',}
    #         ]

    #@TODO
    @property
    def labellist(self):
        if not self.labels:
            return []
        return self.labels

    def _url(self, external=False):
        return url_for('pastebin.paste', slug = self.slug, _external = external)

    @cached_property
    def url(self):
        return self._url()

    @cached_property
    def permalink(self):
        return self._url(True)

