from flask import Flask, g, render_template, flash, redirect, url_for
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)
import forms
import models

app = Flask(__name__)
app.secret_key = 'vasd74p0d@g9uw3rf783ugk?jlbfdzv%iw4kjty8wfits43figufksj3637'

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(user_id):
    try:
        models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None


@app.route('/login/', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Bummer! Your email or password do not match!")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in with your email, {}! :)"
                      .format(form.email.data), "success")
                return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/register/', methods=('GET', 'POST'))
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
            flash("User {} already exists :( ".format(form.email.data),
                  "success")
        else:
            flash("User {} create :) ".format(form.email.data), "success")
            return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/logout', methods=('GET', 'POST'))
def logout():
    logout_user()
    flash("You've been logged out. Come back soon!", "success")
    return redirect(url_for('index'))


@app.route('/')
def index():
    user = models.User.select()
    return render_template('index.html', user=user)


@app.route('/and/entries/', methods=('GET', 'POST'))
# @login_required
def list_entries():
    entries = models.Entry.select()
    return render_template('detail.html', entries=entries)


@app.route('/entries/new', methods=('GET', 'POST'))
@login_required
def entry_create():
    form = forms.EntryForm()
    try:
        models.Entry.create_entry(
            title=form.title.data,
            date=form.date.data,
            time=form.time.data,
            learned=form.learned.data,
            resources=form.resources.data
        )
        flash("You've created a new entry!", "success")
        return redirect(url_for('index'))
    except:
        flash("Entry form NOT valid, sorry bro :(", "warning")
    return render_template('new.html', form=form)


@app.route('/entries/<user_id>', methods=('GET', 'POST'))
# @login_required
def entry_detail(user_id=None):
    user = models.User.get(models.User.username == user_id)
    return render_template('detail.html', user=user)


@app.route('/entries/<user_id>/edit', methods=('GET', 'POST'))
# @login_required
def entry_edit(user_id):
    user = models.User.get(models.User.username == user_id)
    return render_template('edit.html', user=user)


@app.route('/entries/<user_id>/delete', methods=('GET', 'POST'))
# @login_required
def entry_delete(user_id):
    entry = models.User.get(models.User.username == user_id)
    return render_template('delete.html', entry=entry)


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT, host=HOST)
