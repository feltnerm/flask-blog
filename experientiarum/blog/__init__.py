#!/usr/bin/env python

'''
    Blog
'''

from time import mktime
from datetime import datetime, time
from urlparse import urljoin

from flask import Blueprint, request, render_template, redirect, url_for,\
        flash

from flaskext.login import login_required

from werkzeug.contrib.atom import AtomFeed

from experientiarum.extensions import db
from experientiarum.helpers import slugify

from forms import EntryForm
from models import get_by_date, get_by_tags, get_by_slug


blog = Blueprint('blog', __name__, template_folder='templates')

@blog.route('/')
def entries():
    ''' Retrieve and render all non-deleted Entries, and sort them
    in descending order by their pub_date.
    '''
    
    entries = db.Entry.find({'deleted':False}).sort('pub_date', -1)
    return render_template('blog/list.html', entries = entries
            , count = entries.count())

@blog.route('/recent.atom')
def recent_feed():
    feed = AtomFeed('Recent Entries',
                    feed_url=request.url, url=request.url_root)
    entries = db.Entry.find({'deleted':False, 'published':True})\
            .sort('pub_date', -1).limit(15);

    for entry in entries:
        feed.add(entry.title, unicode(entry.body), content_type='html',
                 author='Mark Feltner',
                 url=urljoin(request.url_root, entry.url),
                 updated=entry.edit_date,
                 published=entry.pub_date)
    return feed.get_response()

@blog.route('/e/<slug>')
def entry(slug):
    ''' Find the Entry with the matching slug and return and render it. '''
    
    entry = get_by_slug(slug)
    entries = []
    entries.append(entry)
    return render_template('blog/list.html', entries = entries, count = 1)

#@TODO: Ensure that there are not problems dealing with the slug
@blog.route('/e/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_entry(slug):
    ''' Edit an existing entry. '''

    entry = get_by_slug(slug)
    form = EntryForm(title = entry.title,
                     slug = entry.slug,
                     body = entry.body,
                     tags = entry.get_tags(),
                     pub_date = entry.pub_date,
                     publish = entry.published)

    if form.validate_on_submit():
        # If the title has changed, then change the slug
        if form.title.data != entry.title:
            entry.slug = slugify(form.title.data)
        entry.title = form.title.data
        entry.body = form.body.data
        entry.set_tags(form.tags.data)
        if form.pub_date.data:
            entry.pub_date = datetime.combine(form.pub_date.data, time())
        entry.edit_date = datetime.utcnow()

        if form.publish.data:
            entry.publish = form.publish.data

        if form.delete.data:
            entry.delete = form.delete.data
            entry.delete_date = datetime.utcnow()
        
        entry.save()
        
        flash('Entry edited.')
        return redirect(url_for('blog.entries'))
    return render_template('blog/edit.html', entry = entry, form = form)

#@TODO: Is this still not working?
@blog.route('/e/<slug>/delete', methods=['GET', 'POST'])
@login_required
def delete_entry(slug):
    ''' Delete an existing entry. '''
    
    entry = db.Entry.find_one({'slug':slug}) 
    form = EntryForm(delete = entry.deleted)
    
    if form.validate_on_submit():
        entry.deleted = form.delete.data
        if entry.deleted:
            entry.delete_date = datetime.utcnow()
        
        entry.save()
        
        flash('Entry deleted.')
        return redirect(url_for('blog.entries'))
    return render_template('blog/delete.html', entry=entry, form=form)

#@TODO: Make sure the slug is made properly, and make sure it is checked
# against previous slugs the right way.
@blog.route('/new', methods=['GET', 'POST'])
@login_required
def new_entry():
    ''' Add a entry. '''
    
    form = EntryForm(title = None,
                     body = None,
                     tags = None,
                     pub_date = datetime.utcnow(),
                     publish = True)
    
    if form.validate_on_submit():

        entry = db.Entry()
        entry.title = form.title.data
        entry.slug = slugify(form.title.data)
        # If an entry with this slug already exists, append '2' to make it
        # unique.
        pre_entries = db.Entry.find({'slug': form.slug.data, 'deleted': False})
        if pre_entries.count():
            entry.slug += '-%s' % (pre_entries.count() + 1,)
        entry.body = form.body.data
        entry.set_tags(form.tags.data)
        
        entry.pub_date = form.pub_date.data

        entry.save()
        
        flash('Entry created.')
        return redirect(url_for('blog.entries'))
    return render_template('blog/new.html', form = form)

#@TODO: make it all work.
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
    return render_template('blog/list.html', entries=entries)

#@TODO: make it all work
@blog.route('/t/<tags>')
def tags(tags = None):
    entries = get_by_tags(tags)
    return render_template('blog/list.html', entries=entries
            , count = len(entries))

@blog.route('/deleted')
@blog.route('/deleted/<slug>')
@login_required
def deleted(slug=None):
    entries = []
    if slug:
        entry = db.Entry.find_one({'slug': slug, 'deleted':True})
        entries.append(entry)
    else:
        entries = db.Entry.find({'deleted': True}).sort('pub_date', -1)

    return render_template('/blog/list.html', entries = entries)

@blog.route('/drafts')
@blog.route('/drafs/<slug>')
@login_required
def drafs(slug=None):
    entries = []
    if slug:
        entry = get_by_slug(slug, published=False)
        entries.append(entry)
    else:
        entries = db.Entry.find({'deleted': False
                                 , 'published': False}).sort('pub_date', -1)

    return render_template('/blog/list.html', entries = entries)
        
        
