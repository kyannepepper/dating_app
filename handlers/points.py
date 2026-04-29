import flask
from tinydb import TinyDB, Query
from auth import auth_required

blueprint = flask.Blueprint("points", __name__)
DB_PATH = 'db.json'


def get_user_record(username):
    db = TinyDB(DB_PATH)
    User = Query()
    userTable = db.table('users')
    return userTable, User, userTable.get(User.username == username)


@blueprint.route('/points/increase/<int:amount>', methods=['POST'])
@auth_required
def increase_points(amount):
    username = flask.username
    userTable, User, user = get_user_record(username)

    if not user:
        flask.flash("User not found", "danger")
        return flask.redirect(flask.url_for('login.index'))

    current_points = user.get('points', 0)

    new_points = current_points + amount
    userTable.update({'points': new_points}, User.username == username)
    flask.user['points'] = new_points

    flask.flash(f"You earned {amount} points! Total: {new_points}", "success")
    return flask.redirect(flask.request.referrer or flask.url_for('login.index'))


@blueprint.route('/points/decrease/<int:amount>', methods=['POST'])
@auth_required
def decrease_points(amount):
    username = flask.username
    userTable, User, user = get_user_record(username)

    if not user:
        flask.flash("User not found", "danger")
        return flask.redirect(flask.url_for('login.index'))

    current_points = user.get('points', 0)
    new_points = max(0, current_points - amount)
    userTable.update({'points': new_points}, User.username == username)
    flask.user['points'] = new_points

    flask.flash(f"{amount} points spent. Remaining: {new_points}", "warning")
    return flask.redirect(flask.request.referrer or flask.url_for('login.index'))


@blueprint.route('/points/decreasejson/<int:amount>', methods=['POST'])
@auth_required
def decrease_points_json(amount):
    username = flask.username
    userTable, User, user = get_user_record(username)

    if not user:
        return flask.jsonify({'points': 0})

    current_points = user.get('points', 0)
    new_points = max(0, current_points - amount)
    userTable.update({'points': new_points}, User.username == username)
    
    return flask.jsonify({'points': new_points})


@blueprint.route('/points/increasejson/<int:amount>', methods=['POST'])
@auth_required
def increase_points_json(amount):
    username = flask.username
    userTable, User, user = get_user_record(username)

    if not user:
        return flask.jsonify({'points': 0})

    current_points = user.get('points', 0)
    new_points = current_points + amount
    userTable.update({'points': new_points}, User.username == username)
    
    return flask.jsonify({'points': new_points})

@blueprint.route('/points/get', methods=['POST'])
@auth_required
def get_points():
    username = flask.username
    _, _, user = get_user_record(username)

    if not user:
        flask.flash("User not found", "danger")
        return flask.redirect(flask.url_for('login.index'))

    current_points = user.get('points', 0)

    return flask.jsonify({'points': current_points})
