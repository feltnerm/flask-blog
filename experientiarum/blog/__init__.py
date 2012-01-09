#!/usr/bin/env python

'''
    blog
   
   @todo: pagination 
'''

import re
from datetime import datetime
from unicodedata import normalize

from flask import Blueprint, render_template, abort, request, redirect, \
    url_for, current_app, flash, g
from flask.views import MethodView
from jinja2 import TemplateNotFound


blog = Blueprint('blog', __name__, template_folder='templates')


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug.
    
    @todo: make sure slug is unique"""
    
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


## VIEWS ##
@blog.route('/')
def show_entries():
    ''' Show all entries. '''
    
    entries = g.db.Entry.find({"deleted":False})
    return render_template('entries.html', entries = entries)


@blog.route('/entry/<unique_title>')
def show_entry(unique_title):
    ''' Show a specific entry based on its entry_id. '''
    
    entry = g.db.Entry.one({'unique_title':unique_title, 'deleted':False})
    return render_template('entry.html', entry = entry)


@blog.route('/entry/<unique_title>/edit', methods=['GET', 'PUT'])
def edit_entry(unique_title):
    ''' Edit an existing entry. 
    
    @todo: form validation
    '''
    
    if request.method == 'PUT':
        entry = g.db.Entry.one({'unique_title':unique_title})
        entry.title = request.form['title']
        entry.slug = slugify(entry.title)
        entry.body = request.form['body']
        entry.edit_date = datetime.utcnow()
        
        entry.save()
        
        flash('Entry edited.')
        return redirect(url_for('show_entries'))
    return render_template('edit.html')


@blog.route('/entry/<unique_title>/delete', methods=['GET', 'DELETE'])
def delete_entry(unique_title):
    ''' Delete an existing entry. '''
    
    if request.method == 'DELETE':
        entry = g.db.Entry.one({'unique_title':unique_title})
        entry.deleted = request.form['deleted']
        entry.delete_date = datetime.utcnow()
        
        entry.save()
        
        flash('Entry deleted.')
        return redirect(url_for('show_entries'))
    return render_template('delete.html')


@blog.route('/new', methods=['GET', 'POST'])
def new_entry():
    ''' Add a entry. 
    
    @todo: form validation
    '''
    
    if request.method == 'POST':
        entry = g.db.Entry()
        entry.title = request.form['title']
        entry.slug = slugify(entry.title)
        entry.body = request.form['body']
        entry.pub_date = datetime.utcnow()
        entry.unique_title = '_'.join(entry.pub_date.strftime('%Y%m%d'),entry.slug)
        
        entry.save()
        
        flash('Entry created.')
        return redirect(url_for('show_entries'))
    return render_template('new.html')