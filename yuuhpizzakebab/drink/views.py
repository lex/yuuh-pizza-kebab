from yuuhpizzakebab import app, admin_required, login_required
from .models import Drink
from flask import render_template, session, redirect, url_for, request, flash


@app.route('/drinks', methods=['GET'])
def list_drinks():
    """Shows a list of drinks."""
    return render_template('drink/drinks.html',
                           drinks=Drink.get_all(),
                           selecting=request.args.get('selecting'))


@app.route('/drink/create', methods=['GET', 'POST'])
@admin_required
def create_drink():
    """Creates a new drink.

    Creates a new drink with POST.
    Shows a form to fill with GET.
    """
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
    """Edits a drink.

    arguments:
    drink_id -- id of the drink

    Saves the information with POST.
    Shows a form to edit the contents with GET.
    """
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


@app.route('/drink/delete/<int:drink_id>', methods=['GET'])
@admin_required
def delete_drink(drink_id):
    """Deletes a drink.

    arguments:
    drink_id -- id of the drink
    """
    Drink.delete_by_id(drink_id)
    flash('Removed drink', 'alert-success')

    return redirect(url_for('list_drinks'))
