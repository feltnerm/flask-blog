#!/usr/bin/env python

from flaskext.wtf import Form, TextField, SubmitField, PasswordField, \
    BooleanField, ValidationError, required, optional

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

class RegisterForm(Form):
    
    username = TextField("Username",
                         validators = [required(message="username required")],
                         )
    
    email = TextField("email")
    
    password1 = PasswordField("Password",
                              validators = [required(message="Password required")]
                              )
    
    password2 = PasswordField("Password2",
                              validators = [required(message="Passwords must match")]
                              )
    