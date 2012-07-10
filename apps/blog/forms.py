#!/usr/bin/env python

from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField, \
    BooleanField, SelectField, SelectMultipleField, ValidationError, \
    DateTimeField, required, optional

from apps.extensions import db
from apps.helpers import slugify

#@TODO: come up with your choices for labels and possibly a way to add, edit, delete them.
#@TODO: come up with reasonable field lengths and such

#@TODO: Check into the validate_slug, it'll probably generate some bugs
class EntryForm(Form):
    
    title = TextField("Title",
        validators = [required(message="Title required")])
   
    slug = TextField("Slug")
    tags = TextField("Tags")
    pub_date = DateTimeField("Published On:", id="date-input", format='%Y-%m-%d')
    publish = BooleanField('Publish?')
    delete = BooleanField("Delete?")
    body = TextAreaField("Body", id='text-editor',
        validators = [required(message="Body required")])
    abstract = TextAreaField("Abstract")
    
    
    
    #@TODO: Validate field lengths, types, etc.
    #def validate(self):
    #    pass

    # def validate_slug(self, field):
    #     """ Ensure that the slug provided in the form has not already been
    #     taken. """

    #     if field.data:
    #         slug = slugify(field.data)
    #     else:
    #         slug = slugify(self.title.data)

    #     # Find all entries with the same slug as the one in the form.
    #     # If there is a match, and it is not the same as the entry
    #     # currently being edited, then raise a validation error. Otherwise,
    #     # change the slug. 
    #     entries = db.Entry.find({'slug': slug})
    #     if entries.count():
    #         for entry in entry:
    #             if entry.body == self.body.data:
    #                 field.data = slug
    #             else:
    #                 raise ValidationError, "This slug is taken."
    #     else:
    #         field.data = slug
    

    #def validate_tags(self, field):
    #    ''' Normalize our tags. '''
    #    if field.data:
    #        taglist = [tag.strip() for tag in field.data.split(',')]
    #        tags = ','.join([tag for tag in taglist])
    #        field.data = tags
    #    else:
    #        raise ValidationError, 'Invalid tags. WTF?'

