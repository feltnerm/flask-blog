#!/usr/bin/env python

from flaskext.wtf import Form, TextField, SubmitField, \
    PasswordField, ValidationError, required, optional
from werkzeug.security import generate_password_hash, check_password_hash
from experientiarum.extensions import db

class UserForm(Form):
    
    username = TextField("Username",
                         validators = [required(message="Username required")]
                         )
    
    password1 = PasswordField("Password",
                        validators = [required(message="Password required")]
                              )
    
    password2 = PasswordField("Again",
                        validators = [required(message="Need two to match")]
                            )
    
    submit = SubmitField("Register")
