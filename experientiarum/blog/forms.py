#!/usr/bin/env python

from flaskext.wtf import Form, TextField, TextAreaField, BooleanField, \
    BooleanField, SubmitField, ValidationError, required, email, url, optional

from experientiarum.extensions import db
from experientiarum.helpers import slugify

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
    
    def validate_slug(self):
        ''' Ensure that the slug provided in the form has not already been
        taken. '''
        
        if field.data:
            slug = slugify(field.data)
        else:
            slug = slugify(title)
            
        entries = db.Entry.find({"slug":slug})
        if entries.count():
            raise ValidationError, "This slug is taken."
