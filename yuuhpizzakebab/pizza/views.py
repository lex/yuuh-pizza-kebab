from yuuhpizzakebab import app, admin_required, login_required

from .models import Pizza
from flask import render_template, session, redirect, url_for, request


@app.route('/pizzas')
def list_pizzas():
    return render_template('pizza/pizzas.html',
                           active_tab='pizzas',
                           pizzas=Pizza.get_all())


@app.route('/pizza/create', methods=['GET', 'POST'])
@admin_required
def create_pizza():
    if request.method == 'POST':
        name = request.form['pizza_name']
        price = request.form['pizza_price']
        image_url = request.form['pizza_image_url']

        p = Pizza(None, name, price, image_url, [])
        p.save()

        return redirect(url_for('list_pizzas'))

    return render_template('pizza/create_pizza.html', active_tab='pizzas', )


@app.route('/pizza/edit/<int:pizza_id>', methods=['GET', 'POST'])
@admin_required
def edit_pizza(pizza_id):
    if request.method == 'POST':
        name = request.form['pizza_name']
        price = request.form['pizza_price']
        image_url = request.form['pizza_image_url']

        p = Pizza(pizza_id, name, price, image_url, [])
        p.save()

        return redirect(url_for('list_pizzas'))

    pizza = Pizza.get_by_id(pizza_id)

    if not pizza:
        return redirect(url_for('list_pizzas'))

    return render_template('pizza/edit_pizza.html',
                           active_tab='pizzas',
                           pizza=pizza)


@app.route('/pizza/delete/<int:pizza_id>')
@admin_required
def delete_pizza(pizza_id):
    Pizza.delete_by_id(pizza_id)

    return redirect(url_for('list_pizzas'))
