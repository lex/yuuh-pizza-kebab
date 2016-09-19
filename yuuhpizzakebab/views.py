from yuuhpizzakebab import app
from flask import render_template


@app.route('/')
def home():
    return render_template('index.html', active_tab='home')


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
