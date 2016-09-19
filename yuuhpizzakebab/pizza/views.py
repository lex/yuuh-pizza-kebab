from yuuhpizzakebab import app
from yuuhpizzakebab.pizza.database_functions import get_pizzas
from flask import render_template


@app.route('/pizzas')
def list_pizzas():
    return render_template('pizzas.html',
                           active_tab='pizzas',
                           pizzas=get_pizzas())
