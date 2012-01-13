import re

from datetime import datetime
from unicodedata import normalize

from experientiarum.extensions import db
from experientiarum.helpers import generate_password, check_password
from flask import Blueprint, render_template, abort, request, redirect, \
    url_for, current_app, flash, session, g


from forms import UserForm


users = Blueprint('users', __name__, template_folder='templates')

@users.route('/register/', methods = ['GET', 'POST'])
def register():

    form = UserForm()

    if form.validate_on_submit():
        user = db.User()
        user.username = request.form['username']
        user.pwhash = generate_password(request.form['password1'])

        user.save()

        flash('Registration successful!')
        return redirect(url_for('main.index'))
    return render_template('users/register.html', form=form)

@users.route('/login/', methods = ['GET', 'POST'])
def login():

    form = UserForm()

    if form.validate_on_submit():
        user = db.User.find({'username':request.form['username']})
    
        if check_password(user.pwhash, request.form['password1']):

            session.permanent = form.remember.data

            identity_changed.send(curent_app._get_current_object(),
                                identity=Identity(user.username))
            
            flash('Welcome back, %s' % user.username, 'success')

            return redirect(url_for('main.index'))
        
        else:
            flash('Sorry, invalid login', 'error')

    return render_template('users/login.html', form=form)


@users.route('/logout/', methods = ['GET', 'POST'])
def logout():
    
    pass
