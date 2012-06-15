from datetime import datetime

from flask import Blueprint, render_template, abort, request, redirect, \
    url_for, current_app, flash, session, g

from flask.ext.login import login_user, confirm_login, login_required, \
        logout_user

from apps.extensions import db
from apps.helpers import to_oid

from forms import LoginForm, RegisterForm
from models import authenticate, get_by_username

users = Blueprint('users', __name__) 


@users.route('/login', methods = ['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user, authenticated = authenticate(form.username.data, form.password.data)  
        if authenticated:
            login_user(user, remember=form.remember.data)
            user.last_login = datetime.utcnow()
            user.save()
            return redirect(request.args.get("next") or url_for('main.index'))
        else:
            flash('Sorry, invalid login', 'error')
    return render_template('users/login.html', form=form)


@users.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
   
    logout_user()
    flash(u"You are now logged out.")    
    return redirect(url_for('main.index'))

@users.route('/reauth', methods = ['GET', 'POST'])
def reauth():

    if request.method == 'POST':
        confirm_login()
        flash(u'Reauthenticated')
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('reauth.html')

@users.route('/register', methods = ['GET', 'POST'])
def register():
   
    form = RegisterForm()
    
    if form.validate_on_submit():
        if not get_by_username(form.username.data):
            user = db.User()
            user.username = form.username.data
            user._set_password(form.password1.data)
            user.save()
            login_user(user) 
            flash(u"Welcome %s" % user.username)
           
            return redirect(url_for('main.index'))
        flash('Username %s already taken!' % form.username.data)
    return render_template('users/register.html', form=form)
