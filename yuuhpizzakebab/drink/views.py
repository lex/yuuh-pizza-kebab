from yuuhpizzakebab import app, admin_required, login_required
from .models import Drink
from flask import render_template, session, redirect, url_for, request, flash


@app.route('/drinks')
def list_drinks():
    return render_template('drink/drinks.html', drinks=Drink.get_all())


@app.route('/drink/create', methods=['GET', 'POST'])
@admin_required
def create_drink():
    if request.method == 'POST':
        name = request.form['drink_name']
        price = request.form['drink_price']
        image_url = request.form['drink_image_url']

        d = Drink(None, name, price, image_url)
        success = d.save()

        if not success:
            flash('Some fields need to be filled', 'alert-danger')
            return render_template('drink/edit_drink.html', drink=d)

        flash('Created drink', 'alert-success')
        return redirect(url_for('list_drinks'))

    return render_template('drink/edit_drink.html')


@app.route('/drink/edit/<int:drink_id>', methods=['GET', 'POST'])
@admin_required
def edit_drink(drink_id):
    if request.method == 'POST':
        name = request.form['drink_name']
        price = request.form['drink_price']
        image_url = request.form['drink_image_url']

        k = Drink(drink_id, name, price, image_url)
        k.save()

        return redirect(url_for('list_drinks'))

    drink = Drink.get_by_id(drink_id)

    if not drink:
        return redirect(url_for('list_drinks'))

    return render_template('drink/edit_drink.html', drink=drink)


@app.route('/drink/delete/<int:drink_id>')
@admin_required
def delete_drink(drink_id):
    Drink.delete_by_id(drink_id)

    return redirect(url_for('list_drinks'))
