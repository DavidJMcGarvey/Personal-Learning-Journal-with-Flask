#!/usr/bin/env python

"""Personal Learning Journal w/ FLASK
This is a web app build with Flask that allows user to add journal entries
Journal entries consist of following fields: title, date, time,
what was learned, and resources to remember.

Created: 2019-04-11
Updated: 2019-04-17
Author: David McGarvey"""
from flask import Flask, g, render_template, flash, redirect, url_for
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)
from peewee import *

import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'vasd74p0d@g9uw3rf783ugk?jlbfdzv%iw4kjty8wfits43figufksj3637'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the DATABASE before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the DATABASE connection after each request"""
    g.db.close()
    return response


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Bummer! Your email or password do not match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in with your email, {}! :)"
                      .format(form.email.data), "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        try:
            models.User.create_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )
        except ValueError:
            flash("User with email: {} already exists :( "
                  .format(form.email.data), "success")
        else:
            flash("User with email: {} created :) ".format(form.email.data),
                  "success")
            return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You've been logged out. Come back soon!", "success")
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/entries/', methods=['GET', 'POST'])
def index():
    form = models.Entry.select()
    return render_template('index.html', form=form)


@app.route('/entries/new/', methods=['GET', 'POST'])
@login_required
def entry_create():
    form = forms.EntryForm()
    if form.validate_on_submit():
        try:
            models.Entry.create_entry(
                user=g.user._get_current_object(),
                title=form.title.data,
                date=form.date.data,
                time=form.time.data,
                learned=form.learned.data,
                resources=form.resources.data,
            )
            flash("You've created a new entry!", "success")
            return redirect(url_for('index'))
        except IntegrityError:
            flash("Entry not valid", "error")
    else:
        print("The Title is: {}".format(form.title.data))
    return render_template('new.html', form=form)


@app.route('/entries/<title_id>/', methods=['GET', 'POST'])
@login_required
def entry_detail(title_id):
    form = models.Entry.get(models.Entry.title == title_id)
    return render_template('detail.html', form=form)


@app.route('/entries/<user_id>/edit/', methods=['GET', 'POST'])
@login_required
def entry_edit(user_id):
    user = models.User.get(models.User.username == user_id)
    form = models.Entry.get()
    return render_template('edit.html', user=user, form=form)


@app.route('/entries/<title_id>/delete/', methods=['GET', 'POST'])
@login_required
def entry_delete(title_id):
    models.Entry.get(models.Entry.title == title_id).delete_instance()
    form = models.Entry.select()
    flash("Entry successfully deleted!", "success")
    return render_template('index.html', form=form)


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='Dave',
            email='dave@test.com',
            password='password'
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, port=PORT, host=HOST)
