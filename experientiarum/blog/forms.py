#!/usr/bin/env python

from flaskext.wtf import Form, TextField, TextAreaField, BooleanField, \
    SubmitField, ValidationError, required, email, url, optional

from experientiarum.extensions import db
from experientiarum.helpers import slugify


class EntryForm(Form):
    
    title = TextField("Title",
                      validators = [required(message="Title Required")]
                      )
    
    slug = TextField("Slug")
    
    body = TextField("Body")
    
    tags = TextField("Tags", 
                     validators = [required(message="Tags required")]
                     )
    
    submit = SubmitField("Save")
    
    def __init__(self, *args, **kwargs):
        self.entry = kwargs.get('obj', None)
        super(EntryForm, self).__init__(*args, **kwargs)
    
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