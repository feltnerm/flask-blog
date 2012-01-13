#!/usr/bin/env python

'''
    blog
   
   @todo: pagination 
'''

import re

from datetime import datetime
from unicodedata import normalize

from experientiarum.extensions import db
from experientiarum.helpers import slugify
from forms import EntryForm
from flask import Blueprint, render_template, abort, request, redirect, \
    url_for, current_app, flash, g
from jinja2 import TemplateNotFound


blog = Blueprint('blog', __name__, template_folder='templates')

## VIEWS ##
@blog.route('/')
def show_entries():
    ''' Show all entries. '''
    
    entries = db.Entry.find({"deleted":False})
    return render_template('blog/entries.html', entries = entries)

@blog.route('/entry/<slug>')
def show_entry(slug):
    ''' Show a specific entry based on its entry_id. '''
    
    entry = db.Entry.one({'slug':slug, 'deleted':False})
    if entry:
        return render_template('blog/entry.html', entry = entry)
    abort(404)

@blog.route('/entry/<slug>/edit', methods=['GET', 'PUT'])
def edit_entry(slug):
    ''' Edit an existing entry. 
    
    @todo: form validation
    '''

    form = EntryForm()
    entry = db.Entry.one({'slug':slug})
    
    if form.validate_on_submit():
        entry.title = request.form['title']
        entry.slug = slugify(entry.title)
        entry.body = request.form['body']
        entry.tags = request.form['tags']
        entry.edit_date = datetime.utcnow()
        
        entry.save()
        
        flash('Entry edited.')
        return redirect(url_for('show_entries'))
    return render_template('blog/edit.html', entry=entry, form=form)


@blog.route('/entry/<slug>/delete', methods=['GET', 'DELETE'])
def delete_entry(slug):
    ''' Delete an existing entry. '''
    
    form = EntryForm()
    entry = db.Entry.one({'slug':slug})
    
    if form.validate_on_submit():
        entry.deleted = request.form['deleted']
        entry.delete_date = datetime.utcnow()
        
        entry.save()
        
        flash('Entry deleted.')
        return redirect(url_for('blog.show_entries'))
    return render_template('blog/delete.html', entry=entry, form=form)


@blog.route('/new', methods=['GET', 'POST'])
def new_entry():
    ''' Add a entry. 
    
    @todo: form validation
    '''
    
    form = EntryForm()
    
    if form.validate_on_submit():
        entry = db.Entry()
        entry.title = request.form['title']
        entry.slug = slugify(entry.title)
        entry.body = request.form['body']
        entry.tags = request.form['tags']
        entry.pub_date = datetime.utcnow()
        
        entry.save()
        
        flash('Entry created.')
        return redirect(url_for('show_entries'))
    return render_template('blog/new.html', form=form)

'''
@blog.route('/archives')
@blog.route('/archives/<year>')
@blog.route('/archives/<year>/<month>')
@blog.route('/archives/<year>/<month>/<day>')
@blog.route('/archives/<year>/<month>/<day>/<slug>')
def archive(year = None, month = None, day = None, slug = None):
    dt = datetime.strptime('%s%s%s' % (year,month,day), '%Y%m%d')
    result = g.db.Entry.find({'deleted':False})
    
    for entry in result:
'''
        
