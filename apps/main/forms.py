#!/usr/bin/env python

from flask.ext.wtf import Form, SubmitField, TextAreaField, required

class DerpForm(Form):

    body = TextAreaField('Editor', validators = [required(message="Body required")])
