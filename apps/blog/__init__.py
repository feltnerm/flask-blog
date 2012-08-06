#!/usr/bin/env python

'''
    Blog
'''

from datetime import datetime, time
from urlparse import urljoin

from flask import Blueprint, request, render_template, redirect, url_for,\
        flash

from werkzeug.contrib.atom import AtomFeed

from flask.ext.login import login_required

from apps.extensions import db
from apps.helpers import slugify, markup

from models import get_by_date, get_by_tags, get_by_slug


blog = Blueprint('blog', __name__)


@blog.route('/')
def entries():
    ''' Retrieve and render all non-deleted Entries, and sort them
    in descending order by their pub_date.
    '''
    
    entries = db.Entry.find({'deleted':False, 'published':True}).sort([('pub_date', -1),('_id', -1)])
    return render_template('blog/entries.html', entries = entries)


@blog.route('/e/<slug>')
def entry(slug):
    ''' Find the Entry with the matching slug and return and render it. '''
    
    entry = get_by_slug(slug)
    return render_template('blog/entry.html', entry = entry)

#@TODO: Ensure that there are not problems dealing with the slug
@blog.route('/e/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_entry(slug):
    ''' Edit an existing entry. '''

    error = None
    entry = get_by_slug(slug)
    if request.method == 'POST':

        title = request.form.get('entry-title')
        abstract = request.form.get('entry-abstract')
        tags = request.form.get('entry-tags')
        publish = request.form.get('entry-publish', 'off') == 'on'
        body = request.form.get('entry-body')
        # If the title has changed, then change the slug
        if title != entry.title:
            entry.slug = slugify(title)
        entry.title = title
        entry.abstract = abstract
        entry.body = body
        entry.set_tags(tags)
        entry.edit_date = datetime.utcnow()

        entry.publish = publish

        entry.deleted = request.form.get('entry-delete', 'off') == 'on'

        entry.save()
        
        flash('Entry edited.')
        return redirect(url_for('blog.entries'))
    return render_template('blog/edit.html', entry=entry)


#@TODO: Make sure the slug is made properly, and make sure it is checked
# against previous slugs the right way.
@blog.route('/new', methods=['GET', 'POST'])
@login_required
def new_entry():
    ''' Add a entry. '''
    
    error = None
    if request.method == 'POST':
        title = request.form.get('entry-title')
        abstract = request.form.get('entry-abstract')
        tags = request.form.get('entry-tags')
        publish = request.form.get('entry-publish', 'off') == 'on'
        body = request.form.get('entry-body')

        entry = db.Entry()
        entry.title = title
        entry.abstract = abstract
        entry.slug = slugify(title)
        # If an entry with this slug already exists, append '2' to make it
        # unique.
        pre_entries = db.Entry.find({'slug': entry.slug})
        if pre_entries.count():
            entry.slug += '-%s' % (pre_entries.count() + 1,)
        entry.body = body
        entry.set_tags(tags)
        
        entry.pub_date = datetime.utcnow()

        entry.save()
        
        flash('Entry created.')
        return redirect(url_for('blog.entries'))


    return render_template('blog/new.html')

@blog.route('/recent.atom')
def recent_entries():
    feed = AtomFeed('Recent Entries',
            feed_url=request.url, url=request.url_root)
    entries = db.Entry.find({'deleted':False, 'published':True})\
            .sort('pub_date',-1).limit(15);

    for entry in entries:
        feed.add(entry.title, unicode(entry.body), content_type='html',
                author='Mark Feltner',
                url=urljoin(request.url_root, entry.url),
                updated=entry.pub_date,
                published=entry.pub_date)
    return feed.get_response()

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
def drafs(slug=None):
    entries = []
    if slug:
        entry = get_by_slug(slug, published=False)
        entries.append(entry)
    else:
        entries = db.Entry.find({'deleted': False
                                 , 'published': False}).sort('pub_date', -1)

    return render_template('/blog/list.html', entries = entries)
        
        
