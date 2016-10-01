from sqlalchemy import text
from yuuhpizzakebab import db
from yuuhpizzakebab.user.models import User


def get_user_by_id(user_id):
    t = text(
        'select * from YPKUser where id = :user_id')
    users = db.engine.execute(t, user_id=user_id)

    if not users:
        return None

    for u in users:
        return User(u[0], u[1], u[4])

def get_user(username, password):
    t = text(
        'select * from YPKUser where username = :username and password = :password')
    users = db.engine.execute(t, username=username, password=password)

    if not users:
        return None

    for u in users:
        print(u)
        return User(u[0], u[1], u[4])



def create_user(username, password):
    t = text(
        'insert into YPKUser (username, password) values (:username, :password)')

    db.engine.execute(t, username=username, password=password)

    return get_user(username, password)
