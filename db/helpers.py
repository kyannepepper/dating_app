import tinydb
import hashlib
import flask

def load_db():
    return tinydb.TinyDB('db.json', sort_keys=True, indent=4, separators=(',', ': '))

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_theme_context(user):
    return {
        "font_color": user.get("font_color", "white"),
        "body_color": user.get("body_color", "white"),
        "colors": user.get("colors", []),
        "nav_color": user.get("nav_color", "#308A6F"),
        "nav_body_color": user.get("nav_body_color", "#2f6076")
    }
    
blueprint = flask.Blueprint("colors", __name__)

@blueprint.route('/colors/add', methods=['POST'])
def addColor():
    """Adds a color to the user's list of colors"""
    db = load_db()
    username = flask.request.cookies.get('username')

    if not username:
        flask.flash("You must be logged in to add colors", "danger")
        return flask.redirect(flask.url_for('login.index'))

    # Get user from TinyDB
    user = db.table('users').get(lambda u: u['username'] == username)
    if not user:
        flask.flash("User not found", "danger")
        return flask.redirect(flask.url_for('login.index'))

    new_color = flask.request.form.get("color")
    if not new_color:
        flask.flash("Color cannot be empty", "warning")
        return flask.redirect(flask.request.referrer or flask.url_for('login.index'))

    # Initialize colors if it doesn't exist
    if "colors" not in user:
        user["colors"] = []
    
    # Add color if not already in the list
    if new_color not in user["colors"]:
        user["colors"].append(new_color)
        db.table('users').update(user, doc_ids=[user.doc_id])
        flask.flash(f"Color '{new_color}' added to your collection", "success")
    else:
        flask.flash(f"Color '{new_color}' is already in your collection", "info")
    
    return flask.redirect(flask.request.referrer or flask.url_for('login.index'))

@blueprint.route('/colors/set-font', methods=['POST'])
def setFontColor():
    """Sets the font color from the user's existing colors"""
    db = load_db()
    username = flask.request.cookies.get('username')

    if not username:
        flask.flash("No username found in cookies", "danger")
        return flask.redirect(flask.url_for('login.index'))

    # Get user from TinyDB
    user = db.table('users').get(lambda u: u['username'] == username)
    if not user:
        flask.flash("User not found", "danger")
        return flask.redirect(flask.url_for('login.index'))

    color_value = flask.request.form.get("color")
    if not color_value:
        flask.flash("No color selected", "warning")
        return flask.redirect(flask.request.referrer or flask.url_for('login.index'))

    # Make sure the color exists in the user's colors
    colors = user.get("colors", [])
    if color_value not in colors and colors:
        flask.flash("Selected color is not in your collection", "warning")
        return flask.redirect(flask.request.referrer or flask.url_for('login.index'))

    # Update the font color
    user["font_color"] = color_value
    db.table('users').update({"font_color": color_value}, doc_ids=[user.doc_id])

    flask.flash(f"Font color updated to {color_value}", "success")
    return flask.redirect(flask.request.referrer or flask.url_for('login.index'))

@blueprint.route('/colors/setbody', methods=['POST'])
def setBodyColors():
    db = load_db()
    username = flask.request.cookies.get('username')

    if not username:
        flask.flash("No username found in cookies", "danger")
        return flask.redirect(flask.url_for('login.index'))

    # Get user from TinyDB
    user = db.table('users').get(lambda u: u['username'] == username)
    if not user:
        flask.flash("User not found", "danger")
        return flask.redirect(flask.url_for('login.index'))

    color_type = flask.request.form.get("type")  # font_color or body_color
    color_value = flask.request.form.get("color")  # e.g. #ffcc00

    if color_type not in ['font_color', 'body_color'] or not color_value:
        flask.flash("Invalid input", "warning")
        return flask.redirect(flask.request.referrer or flask.url_for('login.index'))

    # Update the specific color field
    update_data = {color_type: color_value}
    db.table('users').update(update_data, doc_ids=[user.doc_id])

    flask.flash(f"{color_type.replace('_', ' ').capitalize()} updated to {color_value}.", "success")
    return flask.redirect(flask.request.referrer or flask.url_for('login.index'))

@blueprint.route('/colors', methods=['GET'])
def colorSettings():
    """Display color settings page"""
    db = load_db()
    username = flask.request.cookies.get('username')
    
    if not username:
        flask.flash("You must be logged in to view color settings", "danger")
        return flask.redirect(flask.url_for('login.loginscreen'))
    
    # Get user from TinyDB
    user = db.table('users').get(lambda u: u['username'] == username)
    if not user:
        flask.flash("User not found", "danger")
        return flask.redirect(flask.url_for('login.loginscreen'))
    
    # Get user's colors or initialize empty list
    colors = user.get("colors", [])
    
    return flask.render_template('colors.html',
    title="Color Settings",
    current_font_color=user.get("font_color", ""),
    current_body_color=user.get("body_color", ""),
    **get_user_theme_context(user)
)

@blueprint.route('/colors/setnav', methods=['POST'])
def setNavColor():
    """Sets the nav or nav body color from the user's existing colors"""
    db = load_db()
    username = flask.request.cookies.get('username')

    if not username:
        flask.flash("No username found in cookies", "danger")
        return flask.redirect(flask.url_for('login.index'))

    # Fetch user
    user = db.table('users').get(lambda u: u['username'] == username)
    if not user:
        flask.flash("User not found", "danger")
        return flask.redirect(flask.url_for('login.index'))

    color_type = flask.request.form.get("type")  # "nav_color" or "nav_body_color"
    color_value = flask.request.form.get("color")

    if color_type not in ['nav_color', 'nav_body_color'] or not color_value:
        flask.flash("Invalid input", "warning")
        return flask.redirect(flask.request.referrer or flask.url_for('login.index'))

    # Validate the color exists in user's list
    colors = user.get("colors", [])
    if color_value not in colors and colors:
        flask.flash("Selected color is not in your collection", "warning")
        return flask.redirect(flask.request.referrer or flask.url_for('login.index'))

    # Update the nav or nav_body color
    user[color_type] = color_value
    db.table('users').update({color_type: color_value}, doc_ids=[user.doc_id])

    flask.flash(f"{color_type.replace('_', ' ').capitalize()} updated to {color_value}", "success")
    return flask.redirect(flask.request.referrer or flask.url_for('login.index'))