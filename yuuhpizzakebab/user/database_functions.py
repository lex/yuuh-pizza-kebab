from sqlalchemy import text
from yuuhpizzakebab import db
from yuuhpizzakebab.user.models import User


def get_user(username, password):
    t = text(
        'select * from YPKUser where username = :username and password = :password')
    users = db.engine.execute(t, username=username, password=password)

    if not users:
        return None

    for u in users:
        print(u)
        return User(u[0], u[1], u[3])
