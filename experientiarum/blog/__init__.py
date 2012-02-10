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

from flaskext.login import login_required

from experientiarum.extensions import db
from experientiarum.helpers import slugify
from experientiarum.permissions import admin

from forms import EntryForm
from models import get_by_date, get_by_slug, get_by_tags


blog = Blueprint('blog', __name__, template_folder='templates')

## VIEWS ##
@blog.route('/')
def entries():
    ''' Show all entries. '''
    
    entries = db.Entry.find({'deleted':False})
    return render_template('blog/entries.html', entries = entries)

@blog.route('/entry/<slug>')
def entry(slug):
    ''' This should be each entrie's permalink and is optimistically unique'''
    
    entry = get_by_slug(slug)
    return render_template('blog/entry.html', entry = entry)

@blog.route('/entry/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_entry(slug):
    ''' Edit an existing entry. 
    
    @todo: form validation
    '''

    entry = get_by_slug(slug)
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
        return redirect(url_for('blog.entries'))
    return render_template('blog/edit.html', entry=entry, form=form)


@blog.route('/entry/<slug>/delete', methods=['GET', 'POST'])
@login_required
def delete_entry(slug):
    ''' Delete an existing entry. '''
    
    form = EntryForm()
    entry = db.Entry.one({'slug':slug})
    
    if form.validate_on_submit():
        entry.deleted = request.form['deleted']
        entry.delete_date = datetime.utcnow()
        
        entry.save()
        
        flash('Entry deleted.')
        return redirect(url_for('blog.entries'))
    return render_template('blog/delete.html', entry=entry, form=form)


@blog.route('/new', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('blog.entries'))
    return render_template('blog/new.html', form=form)

@blog.route('/archive/<year>')
@blog.route('/archive/<year>/<month>')
@blog.route('/archive/<year>/<month>/<day>')
@blog.route('/archive/<year>/<month>/<day>/<slug>')
def archive(year = None, month = None, day = None, slug = None):
    
    if slug:
        entry = get_by_slug(slug)
        return render_template('blog/entry.html', entry=entry)
    
    entries = get_by_date(year, month, day)
    return render_template('blog/entries.htmml', entries=entries)

@blog.route('/tags/<tags>')
def tags(tags = None):
    entries = get_by_tags(tags)
    return render_template('blog/entries.html', entries=entries)
