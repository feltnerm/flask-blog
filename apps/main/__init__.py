#!/usr/bin/env python

import os.path
from datetime import datetime
from hashlib import md5

from flask import Blueprint, render_template, redirect, url_for

from flask.ext.login import login_required

from forms import DerpForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    about_file_path = os.path.abspath('experientiarum/filedb/about/about.md')
    about_file = open(about_file_path, 'rb')
    body = about_file.read()
    about_file.close()

    return render_template('about.html', body = body)

@main.route('/about/edit', methods=['GET','POST'])
@login_required
def edit_about():

    about_file_path = os.path.abspath('experientiarum/filedb/about/about.md')
    about_file = open(about_file_path, 'rb')
    body = about_file.read()
    about_file.close()

    form = DerpForm(body = body)

    if form.validate_on_submit():
        # Check if the files have changed since the form submission
        form_md5 = md5(form.body.data).digest()
        body_md5 = md5(body).digest()

        # Save the older file in a backup
        if form_md5 != body_md5:
            date = datetime.utcnow().strftime('%H:%M_%y-%j')
            new_file_path = os.path.abspath('experientiarum/filedb/about/backup/%s_about.md' % date)
            with open(new_file_path, 'wb') as new_file:
                new_file.write(body)
            body = form.body.data

            # Write the new projects file
            with open(about_file_path, 'w') as about_file:
                about_file.write(body)

        return redirect(url_for('main.about'))
    
    return render_template('edit_about.html', form = form)

@main.route('/projects')
def projects():

    projects_file_path = os.path.abspath('experientiarum/filedb/projects/projects.md')
    projects_file = open(projects_file_path, 'rb')
    body = projects_file.read()
    projects_file.close()
    
    return render_template('projects.html', body = body)

@main.route('/projects/edit', methods=['GET','POST'])
@login_required
def edit_projects():

    projects_file_path = os.path.abspath('experientiarum/filedb/projects/projects.md')
    projects_file = open(projects_file_path, 'rb')
    body = projects_file.read()
    projects_file.close()

    form = DerpForm(body=body)

    if form.validate_on_submit():
        # Check if the files have changed since the form submission
        form_md5 = md5(form.body.data).digest()
        body_md5 = md5(body).digest()

        # Save the older file in a backup
        if form_md5 != body_md5:
            date = datetime.utcnow().strftime('%H:%M_%y-%j')
            new_file_path = os.path.abspath('experientiarum/filedb/projects/backup/%s_projects.md' % date)
            with open(new_file_path, 'wb') as new_file:
                new_file.write(body)
            body = form.body.data

            # Write the new projects file
            with open(projects_file_path, 'w') as projects_file:
                projects_file.write(body)

        return redirect(url_for('main.projects'))

    return render_template('edit_projects.html', form = form)
