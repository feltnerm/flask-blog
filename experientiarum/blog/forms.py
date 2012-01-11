#!/usr/bin/env python

from flaskext.wtf import Form, TextField, BooleanField


class EditEntryForm(Form):
    
    title = TextField('Title')
    body = TextField('Body')
    deleted = BooleanField('Delete?')


class NewEntryForm(Form):
    
    title = TextField('Title')
    body = TextField('Body')