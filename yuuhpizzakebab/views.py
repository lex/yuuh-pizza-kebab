from yuuhpizzakebab import app
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html', active_tab='home')


@app.route('/about')
def about():
    return render_template('about.html', active_tab='about')


@app.route('/contact')
def contact():
    return render_template('contact.html', active_tab='contact')


