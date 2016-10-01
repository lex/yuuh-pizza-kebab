from yuuhpizzakebab import app, admin_required, login_required
from .models import Topping
from flask import render_template, session, redirect, url_for, request


@app.route('/toppings')
@admin_required
def list_toppings():
    return render_template('topping/toppings.html', toppings=Topping.get_all())


@app.route('/topping/create', methods=['GET', 'POST'])
@admin_required
def create_topping():
    if request.method == 'POST':
        name = request.form['topping_name']
        price = request.form['topping_price']

        t = Topping(None, name, price)
        t.save()

        return redirect(url_for('list_toppings'))

    return render_template('topping/create_topping.html')


@app.route('/topping/edit/<int:topping_id>', methods=['GET', 'POST'])
@admin_required
def edit_topping(topping_id):
    if request.method == 'POST':
        name = request.form['topping_name']
        price = request.form['topping_price']

        t = Topping(topping_id, name, price)
        t.save()

        return redirect(url_for('list_toppings'))

    topping = Topping.get_by_id(topping_id)

    if not topping:
        return redirect(url_for('list_toppings'))

    return render_template('topping/edit_topping.html', topping=topping)


@app.route('/topping/delete/<int:topping_id>')
@admin_required
def delete_topping(topping_id):
    Topping.delete_by_id(topping_id)

    return redirect(url_for('list_toppings'))
