from flask import Flask, render_template, flash, redirect, url_for
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, logout_user, logout_user)

import models

DEBUG = True
PORT = 8080
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'vasd74p0d@g9uw3rf783ugk?jlbfdzv%iw4kjty8wfits43figufksj3637'


@app.route('/')
def index():
    user = models.User.select()
    return render_template('index.html', user=user)


if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT, host=HOST)
