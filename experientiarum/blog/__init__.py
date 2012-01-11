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
from jinja2 import TemplateNotFound

from forms import EditEntryForm, NewEntryForm


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
    return render_template('blog/entries.html', entries = entries)


@blog.route('/entry/<slug>')
def show_entry(slug):
    ''' Show a specific entry based on its entry_id. '''
    
    entry = g.db.Entry.one({'slug':slug, 'deleted':False})
    return render_template('blog/entry.html', entry = entry)


@blog.route('/entry/<slug>/edit', methods=['GET', 'PUT'])
def edit_entry(slug):
    ''' Edit an existing entry. 
    
    @todo: form validation
    '''

    form = EditEntryForm(request.form)
    entry = g.db.Entry.one({'slug':slug})
    
    if request.method == 'PUT':
        entry.title = request.form['title']
        entry.slug = slugify(entry.title)
        entry.body = request.form['body']
        entry.edit_date = datetime.utcnow()
        
        entry.save()
        
        flash('Entry edited.')
        return redirect(url_for('show_entries'))
    return render_template('blog/edit.html', entry=entry, form=form)


@blog.route('/entry/<slug>/delete', methods=['GET', 'DELETE'])
def delete_entry(slug):
    ''' Delete an existing entry. '''
    
    #form = DeleteEntryForm(request.form)
    entry = g.db.Entry.one({'slug':slug})
    
    if request.method == 'DELETE':
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
    
    form = NewEntryForm(request.form)
    
    if request.method == 'POST':
        entry = g.db.Entry()
        entry.title = request.form['title']
        entry.slug = slugify(entry.title)
        entry.body = request.form['body']
        entry.pub_date = datetime.utcnow()
        
        entry.save()
        
        flash('Entry created.')
        return redirect(url_for('show_entries'))
    return render_template('blog/new.html', form=form)

'''
@blog.route('/archives/<year>/<month>/<day>/<slug>')
def archive(year = None, month = None, day = None, slug = None):
    dt = datetime.strptime('%s%s%s' % (year,month,day), '%Y%m%d')
    result = g.db.Entry.find({'deleted':False})
    
    for entry in result:
'''
        