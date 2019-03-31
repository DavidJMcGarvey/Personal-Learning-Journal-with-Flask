from flask import Flask, g, render_template
from flask_login import LoginManager

import users

DEBUG = True
PORT = 8000
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


@app.after_request
def after_request(response):
    g.db.close()
    return response


if __name__ == '__main__':
    users.User.create_user(
        username='Dave',
        email='dave@email.com',
        password='notpassword',
        admin=True
    )
    app.run(debug=DEBUG, port=PORT, host=HOST)
