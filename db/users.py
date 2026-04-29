import tinydb
from tinydb import where
 
def new_user(db, username, hashed_password, first_name, last_name, iq):
    users = db.table('users')
    User = tinydb.Query()
    if users.get(User.username == username):
        return None
    user_record = {
        'first_name': first_name,
        'last_name': last_name,
        'iq': iq,
        'username': username,
        'password': hashed_password,
        'friends': [],
        'points': 100,
        'body_color' : '#fefefe',
        'font_color' : '#000000',
        'nav_color' : '#fefefe',
        'nav_body_color' : "#2f6076",
        'colors' : ['#fefefe', '#000000', '#fefefe', '#2f6076'],
    }
    return users.insert(user_record)

def get_user(db, username, hashed_password):
    user = db.table('users').get(where('username') == username and where('password') == hashed_password)
    return user

def get_user_by_name(db, username):
    return db.table('users').get(where('username') == username)

def delete_user(db, username, password):
    users = db.table('users')
    User = tinydb.Query()
    return users.remove((User.username == username) &
            (User.password == password))

def add_user_friend(db, user, friend):
    users = db.table('users')
    User = tinydb.Query()
    if friend not in user['friends']:
        if users.get(User.username == friend):
            user['friends'].append(friend)
            users.update({'friends': user['friends']}, where('username') == user['username'])
            return 'Friend {} added successfully!'.format(friend), 'success'
        return 'User {} does not exist.'.format(friend), 'danger'
    return 'You are already friends with {}.'.format(friend), 'warning'

def remove_user_friend(db, user, friend):
    users = db.table('users')
    User = tinydb.Query()
    if friend in user['friends']:
        user['friends'].remove(friend)
        users.upsert(user, (User.username == user['username']) &
                (User.password == user['password']))
        return 'Friend {} successfully unfriended!'.format(friend), 'success'
    return 'You are not friends with {}.'.format(friend), 'warning'

def get_user_friends(db, user):
    users = db.table('users')
    User = tinydb.Query()
    friends = []
    for friend in user['friends']:
        friends.append(users.get(User.username == friend))
    return friends
