#!/usr/bin/env python

from models import Entry

from datetime import datetime

from flask import Blueprint, render_template, abort, request, redirect, \
    url_for, current_app
from flask.views import MethodView
from jinja2 import TemplateNotFound


blog = Blueprint('blog', __name__)

# Register models with db
current_app.db.register[Entry]

## VIEWS ##
@blog.route('/')
@blog.route('/<int:year>/<int:month>/<int:date>')
def show_entries(year, month, date):
    ''' Show all entries or only show ones corresponding to a year, month,
     or date'''
    
    pass

@blog.route('/entries/<int:entry_id>')
def show_entry_id(entry_id, methods = ['GET', 'PUT', 'DELETE']):
    ''' Show a specific entry based on its entry_id. '''
    
    pass

@blog.route('/new', methods=['GET', 'POST'])
def new_entry():
    ''' Add a entry. 
    
    @todo: form validation
    '''
    
    if request.method == 'POST':
        entry = Entry()
        entry.title = request.form['title']
        entry.body = request.form['body']
        entry.published = datetime.utcnow()
        entry.comments_enabled = request.form['comments_enabled']
        entry.tags = request.form['tags']
        
        entry.save()
        
        return redirect(url_for('show_entries'))
    return render_template('new.html')
        

@blog.route('/edit/<int:entry_id>', methods=['PUT'])
def edit_entry(entry_id):
    ''' Edit an existing entry. 
    
    @todo: form validation
    '''
    
    if request.method == 'PUT':
        entry = Entry()
        entry.title = request.form['title']
        entry.body = request.form['body']
        entry.edit_date = datetime.utcnow()
        entry.comments_enabled = request.form['comments_enabled']
        entry.tags = request.form['tags']
        
        entry.save()
        
        return redirect(url_for('show_entries'))
    return render_template('edit.html')
    pass

@blog.route('/delete/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    ''' Delete an existing entry. '''
    
    pass
