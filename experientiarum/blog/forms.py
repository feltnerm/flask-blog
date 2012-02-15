#!/usr/bin/env python

from flaskext.wtf import Form, TextField, TextAreaField, SubmitField, \
    BooleanField, ValidationError, required, optional

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
    
    def validate_tags(self, field):
        ''' Normalize our tags. '''
        if field.data:
            taglist = [tag.strip() for tag in field.data.split(',')]
            tags = ','.join([tag for tag in taglist])
            field.data = tags
        else:
            raise ValidationError, 'Invalid tags. WTF?'
    

class NewEntryForm(EntryForm):

    def validate_slug(self, field):
        ''' Ensure that the slug provided in the form has not already been
        taken. '''
        
        if field.data:
            slug = slugify(field.data)
        else:
            slug = slugify(self.title.data)
            
        entries = db.Entry.find({"slug":slug})
        if entries.count(): 
            raise ValidationError, "This slug is taken."
        else:
            field.data = slug

