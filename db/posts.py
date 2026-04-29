import time
import tinydb
from tinydb import where
from db import helpers
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the upload folder exists

def get_posts(db, user):
    posts_table = db.table('posts')

    # Fetch all posts made by the user
    user_posts = posts_table.search(where('user') == user['username'])

    return user_posts

def add_post(db, user, text, iq, image_path=None):
    posts = db.table('posts')
    post_id = len(posts.all()) + 1
    posts.insert({
        'id': post_id,
        'user': user['username'],
        'text': text,
        'image': image_path,
        'iq': iq,
        'comments': [],
        'time': time.time(),
        'likes': 0,
        'dislikes': 0
    })

def add_comment(db, post_id, user, text):
    posts = db.table('posts')
    Post = tinydb.Query()
    post = posts.get(Post.id == post_id)
    if post:
        comments = post.get('comments', [])
        comments.append({'user': user['username'], 'text': text})
        post['comments'] = comments
        posts.update(post, Post.id == post_id)

def add_missing_ids():
    db = helpers.load_db()
    posts_table = db.table('posts')
    posts = posts_table.all()

    next_id = 1
    for post in posts:
        if 'id' not in post:
            posts_table.update({'id': next_id}, where('text') == post['text'])
            print(f"Added 'id' {next_id} to post:", post)
            next_id += 1

if __name__ == "__main__":
    add_missing_ids()
    print("Missing IDs have been added to posts.")
