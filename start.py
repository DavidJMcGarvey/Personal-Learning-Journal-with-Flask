from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user,
                         logout_user, login_required, current_user)

import forms
import users

DEBUG = True
PORT = 8080
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'cadgvnoearg4ks9s?8!dfn38andsvhw34efw4t9g4ujsdfgsjdgw'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return users.User.get(users.User.id == userid)
    except users.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Close the database connection after each request"""
    g.db = users.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/register', methods=("GET", "POST"))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("YES! You registered!", "success")
        users.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = users.User.get(users.User.email == form.email.data)
        except users.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Thanks for using... WHATEVER THIS IS")
    redirect(url_for('index'))


@app.route('/new_post', methods=('GET', 'POST'))
@login_required
def post():
    form = forms.PostForm()
    if form.validate_on_submit():
        users.Post.create(
            user=g.user._get_current_object(),
            content=form.content.data.strip()
        )
        flash("Message posted!", "success")
        return redirect(url_for('index'))
    return render_template('post.html', form=form)


@app.route('/')
def index():
    stream = users.Post.select().limit(10)
    return render_template('stream.html', stream=stream)


@app.route('/stream')
@app.route('/stream/<username>')
def stream(username=None):
    template = 'stream.html'
    if user and username != current_user.username:
        user = users.User.select().where(users.User.username**username).get()
        stream = user.post.limit(10)
    else:
        stream = current_user.get_stream().limit(10)
        user = current_user
    if username:
        template = 'user_stream.html'
    return render_template(template, stream=stream, user=user)


if __name__ == '__main__':
    users.initialize()
    try:
        users.User.create_user(
            username='Dave',
            email='dave@email.com',
            password='notpassword',
            admin=False
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, port=PORT, host=HOST)
