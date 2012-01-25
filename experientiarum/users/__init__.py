from flask import Blueprint, render_template, abort, request, redirect, \
    url_for, current_app, flash, session, g

from flaskext.principal import identity_changed, Identity

from experientiarum.extensions import db

from forms import UserForm


users = Blueprint('users', __name__, template_folder='templates')


@users.route('/login', methods = ['GET', 'POST'])
def login():

    form = UserForm()

    if form.validate_on_submit():
        if authenticate(request.form['username'], request.form['password']):
            session.permanent = form.remember.data
        
            identity_changed.send(current_app._get_current_object(),
                                identity=Identity(request.form['username']))
            
            flash('Welcome back, %s' % request.form['username'], 'success')
        
            return redirect(url_for('main.index'))
        
    else:
        flash('Sorry, invalid login', 'error')

    return render_template('users/login.html', form=form)


@users.route('/logout', methods = ['GET', 'POST'])
def logout():
    
    pass
