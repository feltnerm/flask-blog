'''
Created on Jan 15, 2012

@author: mark
'''
import re

from datetime import datetime

from jinja2 import TemplateNotFound
from flask import Blueprint, render_template, abort, request, redirect, \
    url_for, current_app, flash, g

from flaskext.login import login_required

from experientiarum.extensions import db
from experientiarum.helpers import slugify

from forms import PasteForm
from models import get_by_date, get_by_slug, get_by_labels, get_by_language

pastebin = Blueprint('pastebin', __name__, template_folder='templates')

@pastebin.route('/')
def pastes():
    pastes = db.Paste.find({'deleted':False}).sort('pub_date', -1)
    return render_template('pastebin/list.html', pastes = pastes)

@pastebin.route('/p/<slug>')
def paste(slug):
    
    paste = get_by_slug(slug)
    pastes = []
    pastes.append(paste)
    return render_template('pastebin/list.html', pastes = pastes)

@pastebin.route('/p/<slug>/edit', methods = ['GET','POST'])
@login_required
def edit_paste(slug):
    
    paste = get_by_slug(slug)
    form = PasteForm(title = paste.title,
                    slug = paste.title,
                    body = paste.body,
                    explanation = paste.explanation,
                    language = paste.language,
                    labels = paste.labels,
                    source = paste.source)

    if form.validate_on_submit():
        if form.title.data != paste.title:
            paste.slug = slugify(form.title.data)
        paste.title = form.title.data
        paste.body = form.body.data
        paste.explanation = form.explanation.data
        paste.language = form.language.data
        paste.labels = form.labels.data
        paste.source = form.source.data

        paste.save()
        flash('Paste edited')
        return redirect(url_for('pastebin.pastes'))
    return render_template('pastebin/edit.html', paste = paste, form = form)

@pastebin.route('/p/<slug>/delete', methods = ['GET','POST'])
@login_required
def delete_paste(slug):
    
    paste = db.Paste.find({"slug": slug})
    form = PasteForm(delete = paste.deleted)

    if form.validate_on_submit():
        paste.deleted = form.delete.data
        if paste.deleted:
            paste.delete_date = datetime.utcnow()

        paste.save()

        flash("Paste deleted")
        return redirect(url_for('pastebin.pastes'))
    return render_template('pastebin/delete.html', paste=paste, form=form)

@pastebin.route('/new', methods = ['GET','POST'])
@login_required
def new_paste():
   
    form = PasteForm(title=None,
                     body=None,
                     language=None,
                     labels=None,
                     explain=None,
                     source=None)

    if form.validate_on_submit():

        paste = db.Paste()
        paste.title = form.title.data
        # If a Paste with this slug already exists:
        paste.slug = slugify(form.title.data)
        pre_pastes = db.Paste.find({'slug': form.slug.data, 'deleted': False})
        if pre_pastes.count():
            paste.slug += '-%s' % (pre_pastes.count() +1,)
        paste.body = form.body.data
        paste.explanation = form.explanation.data
        paste.language = form.language.data
        paste.labels = form.labels.data
        paste.source = form.source.data

        paste.save()

        flash("Paste added")
        return redirect(url_for('pastebin.pastes'))
    return render_template('pastebin/new.html', form=form)

@pastebin.route('/l/<labels>')
def paste_labels(labels):
    
    pastes = get_by_labels(labels)
    return render_template('pastebin/pastes.html', pastes=pastes)

@pastebin.route('/t/<language>')
def paste_language(language):
    
    pastes = get_by_language(language)
    return render_template('pastebin/pastes.html', pastes=pastes)
