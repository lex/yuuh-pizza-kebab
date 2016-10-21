import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask import request, redirect, url_for, session


def login_required(f):
    """The decorator for requiring a logged in user."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('username'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """The decorator for requiring a user with administrator privileges."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('login', next=request.url))

        return f(*args, **kwargs)

    return decorated_function


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['DEBUG'] = os.environ.get('DEBUG', False)
db = SQLAlchemy(app)
app.secret_key = os.environ['SECRET_KEY']

import yuuhpizzakebab.views
import yuuhpizzakebab.pizza.views
import yuuhpizzakebab.kebab.views
import yuuhpizzakebab.drink.views
import yuuhpizzakebab.topping.views
import yuuhpizzakebab.order.views
import yuuhpizzakebab.user.views

if __name__ == '__main__':
    app.run(host='0.0.0.0')
