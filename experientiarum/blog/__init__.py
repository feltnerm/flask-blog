#!/usr/bin/env python

'''
    blog
   
   @todo: pagination 
'''

import re

from datetime import datetime

from jinja2 import TemplateNotFound
from flask import Blueprint, render_template, abort, request, redirect, \
    url_for, current_app, flash, g

from experientiarum.extensions import db
from experientiarum.helpers import slugify
from experientiarum.permissions import auth

from forms import EntryForm


blog = Blueprint('blog', __name__, template_folder='templates')

## VIEWS ##
@blog.route('/')
def blog():
    ''' Show all entries. '''
    
    entries = db.Entry.find({'deleted':False})
    return render_template('blog/entries.html', entries = entries)

@blog.route('/entry/<slug>')
def entry(slug):
    ''' Show a specific entry based on its entry_id. '''
    
    entry = db.Entry.one({'slug':slug, 'deleted':False})
    if entry:
        return render_template('blog/entry.html', entry = entry)
    abort(404)

@blog.route('/entry/<slug>/edit', methods=['GET', 'POST'])
@auth.require(401)
def edit_entry(slug):
    ''' Edit an existing entry. 
    
    @todo: form validation
    '''

    entry = db.Entry.one({'slug':slug})
    form = EntryForm(title = entry.title,
                     slug = entry.slug,
                     body = entry.body,
                     tags = entry.tags)
    if form.validate_on_submit():
        entry.title = request.form['title']
        entry.slug = request.form['slug']
        entry.body = request.form['body']
        tags = list()
        for tag in request.form['tags'].split(','):
            tag.strip(' ')
            tags.append(tag)
        entry.tags = tags
        entry.edit_date = datetime.utcnow()
        
        entry.save()
        
        flash('Entry edited.')
        return redirect(url_for('blog.blog'))
    return render_template('blog/edit.html', entry=entry, form=form)


@blog.route('/entry/<slug>/delete', methods=['GET', 'POST'])
@auth.require(401)
def delete_entry(slug):
    ''' Delete an existing entry. '''
    
    form = EntryForm()
    entry = db.Entry.one({'slug':slug})
    
    if form.validate_on_submit():
        entry.deleted = request.form['deleted']
        entry.delete_date = datetime.utcnow()
        
        entry.save()
        
        flash('Entry deleted.')
        return redirect(url_for('blog.blog'))
    return render_template('blog/delete.html', entry=entry, form=form)


@blog.route('/new', methods=['GET', 'POST'])
@auth.require(401)
def new_entry():
    ''' Add a entry. 
    
    @todo: form validation
    '''
    
    form = EntryForm()
    
    if form.validate_on_submit():
        entry = db.Entry()
        entry.title = request.form['title']
        entry.slug = request.form['slug']
        entry.body = request.form['body']
        tags = list()
        for tag in request.form['tags'].split(','):
            tag.strip(' ')
            tags.append(tag)
        entry.tags = tags
        
        entry.save()
        
        flash('Entry created.')
        return redirect(url_for('blog.blog'))
    return render_template('blog/new.html', form=form)


@blog.route('/archive')
@blog.route('/archive/<year>')
@blog.route('/archive/<year>/<month>')
@blog.route('/archive/<year>/<month>/<day>')
@blog.route('/archive/<year>/<month>/<day>/<slug>')
def archive(year = None, month = None, day = None, slug = None):
    pass
