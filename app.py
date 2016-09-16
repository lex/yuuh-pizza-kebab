import os
from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask import render_template
import json

from models import (Pizza, Topping, Kebab, )

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

app.config['DEBUG'] = True


@app.route('/')
def home():
    return render_template('index.html', active_tab='home')


@app.route('/pizza')
def list_pizza():
    return render_template('pizza.html',
                           active_tab='pizza',
                           pizzas=get_pizzas())


@app.route('/kebab')
def list_kebab():
    return render_template('kebab.html',
                           active_tab='kebab',
                           kebabs=get_kebabs())


@app.route('/about')
def about():
    return render_template('about.html', active_tab='about')


@app.route('/contact')
def contact():
    return render_template('contact.html', active_tab='contact')


@app.route('/sign_in')
def sign_in():
    return render_template('signin.html', active_tab='sign_in')


@app.route('/create_account')
def create_account():
    return render_template('createaccount.html', active_tab='create_account')


def get_pizzas():
    result = db.engine.execute('select * from Pizza')
    pizzas = []

    for r in result:
        pizza_id = int(r[0])
        toppings = []

        t = text(
            'select * from Topping where id in (select topping_id from Pizza_Topping where pizza_id = :pizza_id)')
        toppings_results = db.engine.execute(t, pizza_id=pizza_id)

        for t in toppings_results:
            toppings.append(Topping(t[0], t[1], t[2]))

        pizzas.append(Pizza(r[0], r[1], r[2], toppings))

    return pizzas


def get_kebabs():
    result = db.engine.execute('select * from Kebab')
    kebabs = []

    for r in result:
        kebabs.append(Kebab(r[0], r[1], r[2]))

    return kebabs


if __name__ == '__main__':
    app.run(host='0.0.0.0')
