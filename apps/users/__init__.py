from datetime import datetime

from flask import Blueprint, render_template, request, redirect, \
    url_for, current_app, flash

from flask.ext.login import login_user, confirm_login, login_required, \
        logout_user, UserMixin, AnonymousUser

from apps.extensions import bcrypt

users = Blueprint('users', __name__) 


class Anonymous(AnonymousUser):
    username = u'Anonymous'


class User(UserMixin):

    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username


@users.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', 'no') == 'yes' 
        if username != current_app.config['ADMIN_USERNAME']:
            error = 'Invalid username'
        elif not bcrypt.check_password_hash(current_app.config['ADMIN_PASSWORD_HASH'], password):
            error = 'Invalid password'
        else:
            user = User(username)
            if login_user(user, remember=remember):
                flash('You were logged in')
            else:
                flash('Some sort of error occurred?!?!')
            return redirect(request.args.get("next") or url_for('main.index'))
    return render_template('users/login.html', error=error)


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

