#!/usr/bin/env python

from flaskext.wtf import Form, SubmitField, TextAreaField, required

class DerpForm(Form):

    body = TextAreaField('Editor', validators = [required(message="Body required")])
