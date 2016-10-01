from yuuhpizzakebab import app
from flask import render_template, session, redirect, url_for, request, flash
from yuuhpizzakebab.user.database_functions import get_user, create_user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username, password)

        if not user:
            flash('No such username and/or password', 'alert-danger')
            return redirect(url_for('login'))

        session['username'] = user.username
        session['user_id'] = user.id
        session['logged_in'] = True
        session['is_admin'] = user.is_admin

        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    session.pop('logged_in', None)
    session.pop('is_admin', None)

    flash('Successfully logged out', 'alert-info')

    return redirect(url_for('index'))


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = create_user(username, password)

        if not user:
            return redirect(url_for('login'))

        session['username'] = user.username
        session['user_id'] = user.id
        session['logged_in'] = True
        session['is_admin'] = user.is_admin

        return redirect(url_for('index'))

    return render_template('createaccount.html')
