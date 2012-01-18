#!/usr/bin/env python

from flaskext.wtf import Form, TextField, SubmitField, \
    PasswordField, BooleanField, ValidationError, required, optional
from werkzeug.security import generate_password_hash, check_password_hash
from experientiarum.extensions import db

class UserForm(Form):
    
    username = TextField("Username",
                         validators = [required(message="Username required")]
                         )
    
    password = PasswordField("Password",
                        validators = [required(message="Password required")]
                        )
    
    remember = BooleanField("Remember?")
    
    submit = SubmitField("Submit")
