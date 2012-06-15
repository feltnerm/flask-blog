#!/usr/bin/env python

from flaskext.wtf import Form, TextField, SubmitField, PasswordField, \
    BooleanField, required, equal_to

from apps.extensions import db

class LoginForm(Form):
    
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
                              validators = [equal_to("password1", message="Passwords must match")]
                              )
    
    submit = SubmitField("Register")
    
