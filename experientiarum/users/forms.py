#!/usr/bin/env python

from flaskext.wtf import Form, TextField, BooleanField, SubmitField, \
    PasswordField, ValidationError, required, email, url, optional
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
    
    def validate_password(self):
        if password1 != password2:
            raise ValidationError, "Passwords do not match."
