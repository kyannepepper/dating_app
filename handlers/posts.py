import flask
from flask import Blueprint, request, redirect, url_for
from tinydb import Query, where

import os
import time
from werkzeug.utils import secure_filename

from db import posts, helpers, users
from auth import auth_required
from db.posts import add_post  # Ensure this import is correct

blueprint = flask.Blueprint("posts", __name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blueprint.route('/')
def index():
    db = helpers.load_db()

    # Ensure the user is logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    if username is None or password is None:
        return flask.redirect(flask.url_for('login.loginscreen'))

    user = users.get_user(db, username, password)
    if not user:
        flask.flash('Invalid credentials. Please try again.', 'danger')
        resp = flask.make_response(flask.redirect(flask.url_for('login.loginscreen')))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('password', '', expires=0)
        return resp

    # Get posts for the user and their friends
    friends = users.get_user_friends(db, user)
    all_posts = []
    for friend in friends + [user]:
        friend_posts = posts.get_posts(db, friend)
        for post in friend_posts:
            if post not in all_posts:  # Avoid duplicates
                all_posts.append(post)

    # Sort posts by time
    sorted_posts = sorted(all_posts, key=lambda post: post['time'], reverse=True)

    return flask.render_template('feed_page.html', title=copy.title,
                                 subtitle=copy.subtitle, user=user, username=username,
                                 friends=friends, posts=sorted_posts)


@blueprint.route('/comment', methods=['POST'])
def add_comment():
    db = helpers.load_db()
    post_id = flask.request.form.get('post_id')
    friend_username = flask.request.form.get('friend_username')
    comment_text = flask.request.form.get('comment_text')
    username = flask.request.cookies.get('username')

    if not username:
        flask.flash('You must be logged in to comment.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    # Find the post and add the comment to its 'comments' array
    posts_table = db.table('posts')
    post = posts_table.get(where('id') == int(post_id))
    if not post:
        flask.flash('Post not found.', 'danger')
        return flask.redirect(flask.url_for('login.index'))

    # Add the comment to the 'comments' array
    comment = {
        'user': username,
        'text': comment_text,
        'time': time.time()
    }
    post['comments'].append(comment)
    posts_table.update({'comments': post['comments']}, where('id') == int(post_id))

    flask.flash('Comment added successfully!', 'success')
    if (friend_username):
        return flask.redirect(flask.url_for('friends.view_friend', fname=friend_username))
    else:
        return flask.redirect(flask.url_for('login.index'))

@blueprint.route('/post', methods=['POST'])
@auth_required
def post():
    db = helpers.load_db()
    user = flask.user

    text = flask.request.form.get('post')
    photo = flask.request.files.get('photo')
    iq = user.get('iq')

    image_path = None
    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        photo.save(image_path)
        image_path = os.path.relpath(image_path, start='static')

    add_post(db, user, text, iq, image_path)
    flask.flash('Post created successfully!', 'success')
    return flask.redirect(flask.url_for('login.index'))

@blueprint.route('/react', methods=['POST'])
def react_to_post():
    db = helpers.load_db()
    post_id = int(flask.request.form.get('post_id'))  # Ensure post_id is an integer
    reaction = flask.request.form.get('reaction')
    username = flask.request.cookies.get('username')
    friend_username = flask.request.form.get('friend_username')

    if not username:
        flask.flash('You must be logged in to react.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    # Access the 'posts' table
    posts_table = db.table('posts')

    # Find the post by its ID
    post = posts_table.get(where('id') == post_id)
    if not post:
        flask.flash('Post not found.', 'danger')
        return flask.redirect(flask.url_for('login.index'))

    # Update the reaction count
    if reaction == 'like':
        post['likes'] += 1
    elif reaction == 'dislike':
        post['dislikes'] += 1

    # Save the updated post back to the database
    posts_table.update(post, where('id') == post_id)

    flask.flash('Reaction added successfully!', 'success')
    if (friend_username):
        return flask.redirect(flask.url_for('friends.view_friend', fname=friend_username))
    else:
        return flask.redirect(flask.url_for('login.index'))