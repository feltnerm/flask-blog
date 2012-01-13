#!/usr/bin/env python

from flaskext.wtf import Form, TextField, TextAreaField, BooleanField, \
    BooleanField, SubmitField, ValidationError, required, email, url, optional

from experientiarum.extensions import db
from experientiarum.helpers import slugify
from experientiarum.blog.models import Entry

class EntryForm(Form):
    
    title = TextField("Title",
                      validators = [required(message="Title Required")]
                      )
    
    slug = TextField("Slug")
    
    body = TextAreaField("Body")
    
    tags = TextField("Tags", 
                     validators = [required(message="Tags required")]
                     )
    
    delete = BooleanField("Delete")
    
    submit = SubmitField("Save")
    '''
    def __init__(self, *args, **kwargs):
        self.entry = kwargs.get('obj', None)
        super(EntryForm, self).__init__(*args, **kwargs)
    
    def validate_slug(self, field):
        slug = slugify(field.data)
        if field.data:
            slug = slugify(field.data)
        else:
            slug = slugify(self.title.data)

        entries = db.Entry.find({'slug':slug})
        if self.entry:
            entries = entries.find({'object_id': { '$ne' : self.entry.object_id} })
        if entries.count():
            if field.data:
                error = "This slug is taken"
            else:
                error = "Slug is required."
            raise ValidationError, error
    '''
    '''            
    def validate_slug(self, field):
        if len(field.data) > 50:
            raise ValidationError, "Slug must be less than 50 characters"
        slug = slugify(field.data) if field.data else slugify(self.title.data)[:50]
        entries = db.Entry.find({'slug':slug})
        posts = Entry.query.filter_by(slug=slug)
        if self.post:
            entries = posts.filter(db.not_(Post.id==self.post.id))
        if entries.count():
            error = "This slug is taken" if field.data else "Slug is required"
            raise ValidationError, error
    '''
