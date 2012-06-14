#!/usr/bin/env python

from flaskext.wtf import Form, TextField, TextAreaField, SubmitField, \
        SelectField, SelectMultipleField, BooleanField, ValidationError, \
        required, optional

from experientiarum.extensions import db
from experientiarum.helpers import slugify

LANG_CHOICES = [
    ('cpp','C++'),
    ('py','Python'),
    ('bash','Bash'),
    ('sql','SQL'),
    ('js','Javascript')
    ]

LABEL_CHOICES = [
    ('web','Web'),
    ('scripts','Scripts'),
    ('math','Math'),
    ('server','Server Admin'),
    ('fun','Fun')
    ]


class PasteForm(Form):

    title = TextField('Title', validators = [required(message="Title required")])
    slug = TextField('Slug')
    body = TextAreaField('Body', validators = [required(message="Code required")])
    language = SelectField('Language', choices=LANG_CHOICES
        , validators = [required(message="Language required")])
    explanation = TextField('Explain'
        , validators = [required(message="Explanation required")])
    labels = SelectMultipleField('Labels', choices=LABEL_CHOICES
        , validators = [required(message="Label(s) required")])
    source = TextField('Source')
    deleted = BooleanField('Delete?')

    submit = SubmitField('Save')

    #@TODO: validate field lengths, types, etc.
    # def validate_slug(self, field):
    #     if field.data:
    #         slug = slugify(field.data)
    #     else:
    #         slug = slugify(self.title.data)

    #     pastes = db.Paste.find({"slug": slug})
    #     if pastes.count():
    #         raise ValidationError, "This slug is taken."
    #     else:
    #         field.data = slug

    # def validate_labels(self, field):
    #     pass
