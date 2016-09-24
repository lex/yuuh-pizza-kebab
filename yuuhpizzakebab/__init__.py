import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['DEBUG'] = os.environ.get('DEBUG', False)
db = SQLAlchemy(app)
app.secret_key = os.environ['SECRET_KEY']

import yuuhpizzakebab.views
import yuuhpizzakebab.pizza.views
import yuuhpizzakebab.kebab.views
import yuuhpizzakebab.drink.views
import yuuhpizzakebab.user.views

if __name__ == '__main__':
    app.run(host='0.0.0.0')
