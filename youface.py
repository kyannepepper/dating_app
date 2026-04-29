# std imports
import time
import os

# installed imports
import flask
import timeago
from db import users, helpers
from db import posts as posts_db

# handlers
from handlers import friends, login, posts, copy, points
from auth import auth_required

app = flask.Flask(__name__)

@app.context_processor
def inject_theme():
    if hasattr(flask, 'user'):
        user = flask.user
        return helpers.get_user_theme_context(user)
    return {}

@app.template_filter('convert_time')
def convert_time(ts):
    """A jinja template helper to convert timestamps to timeago."""
    return timeago.format(ts, time.time())

        
        
def register_templates(app):
    """Dynamically registers all HTML templates in a folder as routes.

    Args:
        app: The Flask application instance.
        template_folder: The path to the folder containing the HTML templates.
    """
    for file in os.listdir("templates"):
        if (file == 'base.html'):
            continue
        if (not "_page" in file):
            continue

        if file.endswith(".html"):
            route_name = file[:-5]
            route_path = '/' + file.replace('_page.html', '')

            @auth_required
            def view_func(*args, **kwargs):
                db = helpers.load_db()
                username = flask.username
                user = flask.user

                first_name = user['first_name']
                last_name = user['last_name']
                iq = user['iq']
                friends = users.get_user_friends(db, user) 
                points = user['points'] 
                theme = helpers.get_user_theme_context(user)  
                my_posts = posts_db.get_posts(db, user)
                file = flask.request.path.replace('/', '') + "_page.html"

                all_posts = []
                for friend in friends + [user]:
                    all_posts += posts_db.get_posts(db, friend)
                # sort posts
                sorted_posts = sorted(all_posts, key=lambda post: post['time'], reverse=True)

                return flask.render_template(
                    file,
                    title=copy.title,
                    subtitle=copy.subtitle,
                    user=user,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    friends=friends,
                    iq=iq,
                    points=points,
                    my_posts=my_posts,
                    posts=sorted_posts,
                    **theme
                )

            view_func.__name__ = route_name

            app.add_url_rule(route_path, view_func.__name__, view_func)


register_templates(app)

app.register_blueprint(friends.blueprint)
app.register_blueprint(login.blueprint)
app.register_blueprint(posts.blueprint)
app.register_blueprint(points.blueprint)
app.register_blueprint(helpers.blueprint)

app.secret_key = 'mygroup'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.run(debug=True, host='0.0.0.0')
