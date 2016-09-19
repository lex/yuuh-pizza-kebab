from yuuhpizzakebab import app
from yuuhpizzakebab.drink.database_functions import get_drinks
from flask import render_template


@app.route('/drinks')
def list_drinks():
    return render_template('drinks.html',
                           active_tab='drinks',
                           drinks=get_drinks())
