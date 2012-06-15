#!/usr/bin/env python

from flaskext.wtf import Form, SubmitField, TextAreaField, required

class DerpForm(Form):

    body = TextAreaField('Projects', validators = [required(message="Body required")])
