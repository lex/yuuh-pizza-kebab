from yuuhpizzakebab import app, admin_required, login_required

from .models import Pizza, Topping
from flask import render_template, session, redirect, url_for, request, flash


@app.route('/pizzas')
def list_pizzas():
    return render_template('pizza/pizzas.html', pizzas=Pizza.get_all())


@app.route('/pizza/create', methods=['GET', 'POST'])
@admin_required
def create_pizza():
    if request.method == 'POST':
        name = request.form['pizza_name']
        price = request.form['pizza_price']
        image_url = request.form['pizza_image_url']

        selected_toppings = request.form.getlist('toppings')

        p = Pizza(None, name, price, image_url, [])
        success = p.save()

        if not success:
            flash('Some fields need to be filled', 'alert-danger')
            return render_template('pizza/edit_pizza.html',
                                   pizza=pizza,
                                   available_toppings=Topping.get_all())

        for t in selected_toppings:
            topping_id = int(t)
            p.add_topping(topping_id)

        return redirect(url_for('list_pizzas'))

    return render_template('pizza/edit_pizza.html',
                           available_toppings=Topping.get_all())


@app.route('/pizza/edit/<int:pizza_id>', methods=['GET', 'POST'])
@admin_required
def edit_pizza(pizza_id):
    if request.method == 'POST':
        name = request.form['pizza_name']
        price = request.form['pizza_price']
        image_url = request.form['pizza_image_url']

        selected_toppings = request.form.getlist('toppings')

        p = Pizza(pizza_id, name, price, image_url, [])
        success = p.save()

        if not success:
            flash('Some fields need to be filled', 'alert-danger')
            return render_template('pizza/edit_pizza.html',
                                   pizza=p,
                                   available_toppings=Topping.get_all())

        p.remove_toppings()

        for t in selected_toppings:
            topping_id = int(t)
            p.add_topping(topping_id)

        return redirect(url_for('list_pizzas'))

    pizza = Pizza.get_by_id(pizza_id)

    if not pizza:
        return redirect(url_for('list_pizzas'))

    return render_template('pizza/edit_pizza.html',
                           pizza=pizza,
                           available_toppings=Topping.get_all())


@app.route('/pizza/delete/<int:pizza_id>')
@admin_required
def delete_pizza(pizza_id):
    Pizza.delete_by_id(pizza_id)
    flash('Removed pizza', 'alert-success')

    return redirect(url_for('list_pizzas'))
