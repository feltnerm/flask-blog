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

from forms import EntryForm, NewEntryForm
from models import get_by_date, get_by_slug, get_by_tags


blog = Blueprint('blog', __name__, template_folder='templates')

## VIEWS ##
@blog.route('/')
@blog.route('/e')
def entries():
    ''' Show all entries. '''
    
    entries = db.Entry.find({'deleted':False})
    return render_template('blog/entries.html', entries = entries)

@blog.route('/e/<slug>')
def entry(slug):
    ''' This should be each entry's permalink and is optimistically unique'''
    
    entry = get_by_slug(slug)
    return render_template('blog/entry.html', entry = entry)

@blog.route('/e/<slug>/edit', methods=['GET', 'POST'])
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
    if form.is_submitted():
        if form.title.data != entry.title:
            entry.slug = slugify(form.title.data)
        entry.title = form.title.data
        entry.body = form.body.data
        entry.tags = form.tags.data
        entry.edit_date = datetime.utcnow()
        
        entry.save()
        
        flash('Entry edited.')
        return redirect(url_for('blog.entries'))
    return render_template('blog/edit.html', entry=entry, form=form)


@blog.route('/e/<slug>/delete', methods=['GET', 'POST'])
@login_required
def delete_entry(slug):
    ''' Delete an existing entry. '''
    
    entry = get_by_slug(slug)
    form = EntryForm(delete = entry.deleted)
    
    if form.validate_on_submit():
        entry.deleted = form.delete.data
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
    
    form = NewEntryForm()
    
    if form.validate_on_submit():
        entry = db.Entry()
        entry.title = form.title.data
        entry.slug = form.slug.data
        entry.body = form.body.data
        entry.tags = form.tags.data
        
        entry.save()
        
        flash('Entry created.')
        return redirect(url_for('blog.entries'))
    return render_template('blog/new.html', form=form)

@blog.route('/archive')
@blog.route('/archive/<year>')
@blog.route('/archive/<year>/<month>')
@blog.route('/archive/<year>/<month>/<day>')
@blog.route('/archive/<year>/<month>/<day>/<slug>')
def archive(year = None, month = None, day = None, slug = None):
    
    if slug:
        entry = get_by_slug(slug)
        return render_template('blog/entry.html', entry=entry)
    
    entries = get_by_date(year, month, day)
    return render_template('blog/entries.html', entries=entries)

@blog.route('/tags/<tags>')
def tags(tags = None):
    entries = get_by_tags(tags)
    return render_template('blog/entries.html', entries=entries)
