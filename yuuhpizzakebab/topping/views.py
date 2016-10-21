from yuuhpizzakebab import app, admin_required, login_required
from .models import Topping
from flask import render_template, session, redirect, url_for, request


@app.route('/toppings', methods=['GET'])
@admin_required
def list_toppings():
    """Shows a list of toppings"""
    return render_template('topping/toppings.html', toppings=Topping.get_all())


@app.route('/topping/create', methods=['GET', 'POST'])
@admin_required
def create_topping():
    """Creates a new drink.

    Administrator rights required.

    Creates a new topping with POST.
    Shows a form to fill with GET.
    """
    if request.method == 'POST':
        name = request.form['topping_name']
        price = request.form['topping_price']

        t = Topping(None, name, price)
        t.save()

        return redirect(url_for('list_toppings'))

    return render_template('topping/edit_topping.html')


@app.route('/topping/edit/<int:topping_id>', methods=['GET', 'POST'])
@admin_required
def edit_topping(topping_id):
    """Edits a topping.

    arguments:
    topping_id -- id of the topping

    Saves the information with POST.
    Shows a form to edit the contents with GET.
    """
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


@app.route('/topping/delete/<int:topping_id>', methods=['GET'])
@admin_required
def delete_topping(topping_id):
    """Deletes a topping.

    arguments:
    topping_id -- id of the topping
    """
    Topping.delete_by_id(topping_id)

    return redirect(url_for('list_toppings'))
