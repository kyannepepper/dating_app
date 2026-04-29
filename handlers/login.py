import flask

from handlers import copy
from db import posts, users, helpers

blueprint = flask.Blueprint("login", __name__)

@blueprint.route('/loginscreen')
def loginscreen():
    """Present a form to the user to enter their username and password."""
    db = helpers.load_db()

    # First check if already logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    if username is not None and password is not None:
        if users.get_user(db, username, password):
            # If they are logged in, redirect them to the feed page
            flask.flash('You are already logged in.', 'warning')
            return flask.redirect(flask.url_for('login.index'))

    return flask.render_template('login.html', title=copy.title,
            subtitle=copy.subtitle)

@blueprint.route('/login', methods=['POST'])
def login():
    """Log in the user.

    Using the username and password fields on the form, create, delete, or
    log in a user, based on what button they click.
    """
    db = helpers.load_db()

    if (flask.request.form.get('new_username')):
        username = flask.request.form.get('new_username')
        password = flask.request.form.get('new_password')
    else:
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')

    hashed_password = helpers.hash_password(password)

    resp = flask.make_response(flask.redirect(flask.url_for('login.index')))
    resp.set_cookie('username', username)
    resp.set_cookie('password', hashed_password)

    submit = flask.request.form.get('type')
    if submit == 'Create Account':
        first_name = flask.request.form.get('new_first_name')
        last_name = flask.request.form.get('new_last_name')
        iq = flask.request.form.get('new_iq')

        if users.new_user(db, username, hashed_password, first_name, last_name, iq) is None:
            resp.set_cookie('username', '', expires=0)
            resp.set_cookie('password', '', expires=0)
            flask.flash('Username {} already taken!'.format(username), 'danger')
            return flask.redirect(flask.url_for('login.loginscreen'))
        flask.flash('User {} created successfully!'.format(username), 'success')
    elif submit == 'Login':
        if users.get_user(db, username, hashed_password):
            flask.flash('Logged in successfully!', 'success')
        else:
            resp.set_cookie('username', '', expires=0)
            resp.set_cookie('password', '', expires=0)
            flask.flash('Invalid username or password!', 'danger')
            return flask.redirect(flask.url_for('login.loginscreen'))
    elif submit == 'Delete':
        if users.delete_user(db, username, hashed_password):
            resp.set_cookie('username', '', expires=0)
            resp.set_cookie('password', '', expires=0)
            flask.flash('User {} deleted successfully!'.format(username), 'success')

    return resp
    
@blueprint.route('/logout', methods=['POST'])
def logout():
    """Log out the user."""
    db = helpers.load_db()

    resp = flask.make_response(flask.redirect(flask.url_for('login.loginscreen')))
    resp.set_cookie('username', '', expires=0)
    resp.set_cookie('password', '', expires=0)
    return resp

@blueprint.route('/')
def index():
    """Serves the main feed page for the user."""
    db = helpers.load_db()

    # make sure the user is logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    if username is None and password is None:
        return flask.redirect(flask.url_for('login.loginscreen'))
    user = users.get_user(db, username, password)
    if not user:
        flask.flash('Invalid credentials. Please try again.', 'danger')
        resp = flask.make_response(flask.redirect(flask.url_for('login.loginscreen')))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('password', '', expires=0)
        return resp

    # get the info for the user's feed
    friends = users.get_user_friends(db, user)
    all_posts = []
    for friend in friends + [user]:
        all_posts += posts.get_posts(db, friend)
    # sort posts
    sorted_posts = sorted(all_posts, key=lambda post: post['time'], reverse=True)
    
    theme = helpers.get_user_theme_context(user)
    return flask.render_template('feed_page.html', title=copy.title,
            subtitle=copy.subtitle, user=user, username=username,
            friends=friends, posts=sorted_posts, **theme)

# Example implementation of users.get_user and users.new_user

