from functools import wraps
import flask
from db import users, helpers

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        db = helpers.load_db()
        username = flask.request.cookies.get('username')
        password = flask.request.cookies.get('password')

        if not username or not password:
            flask.flash('You must be logged in to access this page.', 'danger')
            return flask.redirect(flask.url_for('login.loginscreen'))

        user = users.get_user(db, username, password)
        if not user:
            flask.flash('Invalid credentials. Please log in again.', 'danger')
            resp = flask.make_response(flask.redirect(flask.url_for('login.loginscreen')))
            resp.set_cookie('username', '', expires=0)
            resp.set_cookie('password', '', expires=0)
            return resp

        flask.username = username
        flask.user = user
        return f(*args, **kwargs)
    return decorated_function