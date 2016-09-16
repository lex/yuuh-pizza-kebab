from yuuhpizzakebab import app
import yuuhpizzakebab.database_functions as db_functions
from flask import render_template


@app.route('/')
def home():
    return render_template('index.html', active_tab='home')


@app.route('/pizza')
def list_pizza():
    return render_template('pizza.html',
                           active_tab='pizza',
                           pizzas=db_functions.get_pizzas())


@app.route('/kebab')
def list_kebab():
    return render_template('kebab.html',
                           active_tab='kebab',
                           kebabs=db_functions.get_kebabs())


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
