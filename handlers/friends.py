import flask

from handlers import copy
from db import posts, users, helpers
from auth import auth_required

blueprint = flask.Blueprint("friends", __name__)

@blueprint.route('/addfriend', methods=['POST'])
@auth_required
def addfriend():
    db = helpers.load_db()
    user = flask.user

    friend_name = flask.request.form.get('name')
    if not friend_name:
        flask.flash('Please enter a username to add as a friend.', 'danger')
        return flask.redirect(flask.url_for('login.index'))

    # Check if the friend exists in the database
    friend = users.get_user_by_name(db, friend_name)
    if not friend:
        flask.flash('User not found.', 'danger')
        return flask.redirect(flask.url_for('login.index'))

    message, category = users.add_user_friend(db, user, friend_name)
    flask.flash(message, category)

    return flask.redirect(flask.url_for('login.index'))

@blueprint.route('/unfriend', methods=['POST'])
@auth_required
def unfriend():
    """Removes a user from the user's friends list."""
    db = helpers.load_db()

    user = flask.user

    name = flask.request.form.get('name')
    msg, category = users.remove_user_friend(db, user, name)

    flask.flash(msg, category)
    return flask.redirect(flask.url_for('login.index'))

@blueprint.route('/friend/<fname>')
@auth_required
def view_friend(fname):
    """View the page of a given friend."""
    db = helpers.load_db()

    user = flask.user
    username = flask.username

    friend = users.get_user_by_name(db, fname)
    all_posts = posts.get_posts(db, friend)[::-1] # reverse order

    return flask.render_template('friend.html', title=copy.title,
            subtitle=copy.subtitle, user=user, username=username,
            friend=friend['first_name'],
            friend_username=friend['username'],
            friends=users.get_user_friends(db, user), posts=all_posts)

@blueprint.route('/friends')
def friends_home():
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
    theme = helpers.get_user_theme_context(user)
    return flask.render_template('friends.html', title=copy.title,
            subtitle=copy.subtitle, user=user, username=username,
            friends_home=True, **theme)