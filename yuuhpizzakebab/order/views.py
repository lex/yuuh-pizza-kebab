from yuuhpizzakebab import app, admin_required, login_required
from .models import Order
from yuuhpizzakebab.pizza.models import Pizza
from yuuhpizzakebab.kebab.models import Kebab
from yuuhpizzakebab.drink.models import Drink
from yuuhpizzakebab.user.database_functions import get_user_by_id
from flask import render_template, session, redirect, url_for, request, flash
import datetime


def get_pizzas_from_session():
    """Gets a list of pizzas saved in the user's session."""
    pizzas = []

    if session.get('selected_pizzas'):
        for pizza_id in session.get('selected_pizzas'):
            p = Pizza.get_by_id(pizza_id)
            pizzas.append(p)

    return pizzas


def get_kebabs_from_session():
    """Gets a list of kebabs saved in the user's session."""
    kebabs = []

    if session.get('selected_kebabs'):
        for kebab_id in session['selected_kebabs']:
            k = Kebab.get_by_id(kebab_id)
            kebabs.append(k)

    return kebabs


def get_drinks_from_session():
    """Gets a list of drinks saved in the user's session."""
    drinks = []

    if session.get('selected_drinks'):
        for drink_id in session['selected_drinks']:
            d = Drink.get_by_id(drink_id)
            drinks.append(d)

    return drinks


def get_total_price_of_items(pizzas, kebabs, drinks):
    """Calculates and returns the total price of items provided.

    arguments:
    pizzas - list of pizzas
    kebabs - list of kebabs
    drinks - list of drinks
    """
    total = 0.0

    for p in pizzas:
        total += float(p.price_without_dollar_sign())

    for k in kebabs:
        total += float(k.price_without_dollar_sign())

    for d in drinks:
        total += float(d.price_without_dollar_sign())

    return total


def get_delivery_address():
    """Returns the delivery address saved in the user's session."""
    return session.get('delivery_address')


def clear_session():
    """Clears the user's session of any order related data."""
    session.pop('selected_pizzas', None)
    session.pop('selected_kebabs', None)
    session.pop('selected_drinks', None)
    session.pop('delivery_address', None)


@app.route('/new_order', methods=['GET'])
@login_required
def new_order():
    """Shows the active order."""
    pizzas = get_pizzas_from_session()
    kebabs = get_kebabs_from_session()
    drinks = get_drinks_from_session()
    total_price = get_total_price_of_items(pizzas, kebabs, drinks)
    delivery_address = get_delivery_address()

    return render_template('order/create_order.html',
                           pizzas=pizzas,
                           kebabs=kebabs,
                           drinks=drinks,
                           total_price=total_price,
                           delivery_address=delivery_address)


@app.route('/select/<string:item_type>', methods=['GET'])
@login_required
def select_item(item_type):
    """Redirects the user to select an item of specified type.

    arguments:
    item_type - type of the item (pizza, kebab or drink)
    """
    if item_type not in ['pizza', 'kebab', 'drink']:
        flash('Unknown item type', 'alert-warning')
        return redirect(url_for('new_order'))

    return redirect(url_for('list_{}s'.format(item_type), selecting=True))


@app.route('/select/pizza/<int:pizza_id>', methods=['GET'])
@login_required
def select_pizza(pizza_id):
    """Adds a selected pizza to the user's session.

    arguments:
    pizza_id - id of the pizza
    """
    if not session.get('selected_pizzas'):
        session['selected_pizzas'] = []

    new_list = session['selected_pizzas']
    new_list.append(pizza_id)
    session['selected_pizzas'] = new_list

    return redirect(url_for('new_order'))


@app.route('/select/kebab/<int:kebab_id>', methods=['GET'])
@login_required
def select_kebab(kebab_id):
    """Adds a selected kebab to the user's session.

    arguments:
    kebab_id - id of the kebab
    """
    if not session.get('selected_kebabs'):
        session['selected_kebabs'] = []

    new_list = session['selected_kebabs']
    new_list.append(kebab_id)
    session['selected_kebabs'] = new_list

    return redirect(url_for('new_order'))


@app.route('/select/drink/<int:drink_id>', methods=['GET'])
@login_required
def select_drink(drink_id):
    """Adds a selected drink to the user's session.

    arguments:
    drink_id - id of the drink
    """
    if not session.get('selected_drinks'):
        session['selected_drinks'] = []

    new_list = session['selected_drinks']
    new_list.append(drink_id)
    session['selected_drinks'] = new_list

    return redirect(url_for('new_order'))


@app.route('/place_order', methods=['GET'])
@login_required
def place_order():
    """Places an order for the user with the selected goods and the delivery address."""
    pizzas = get_pizzas_from_session()
    kebabs = get_kebabs_from_session()
    drinks = get_drinks_from_session()
    total_price = get_total_price_of_items(pizzas, kebabs, drinks)

    user_id = session['user_id']
    user = get_user_by_id(user_id)
    ordered_at = datetime.datetime.utcnow()
    delivery_address = get_delivery_address()
    # Delivery is always in an hour for now.
    delivery_at = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    lunch_offer_active = False

    o = Order(None, user, ordered_at, delivery_address, delivery_at, False,
              False, lunch_offer_active)
    o.save()

    for p in pizzas:
        o.add_pizza(p)

    for k in kebabs:
        o.add_kebab(k)

    for d in drinks:
        o.add_drink(d)

    clear_session()

    flash('Order placed', 'alert-success')

    return redirect(url_for('list_orders'))


@app.route('/clear_order', methods=['GET'])
@login_required
def clear_order():
    """Clears all order related information from the session."""
    clear_session()
    return redirect(url_for('new_order'))


@app.route('/orders', methods=['GET'])
@admin_required
def list_orders():
    """Shows a list of orders.

    Requires administrator privileges.
    """
    return render_template('order/orders.html', orders=Order.get_all())


@app.route('/orders/active', methods=['GET'])
@admin_required
def list_active_orders():
    """Shows a list of active (not rejected or delivered) orders.

    Requires administrator privileges.
    """
    return render_template('order/orders.html', orders=Order.get_all_active())


@app.route('/order/<int:order_id>', methods=['GET'])
@admin_required
def order_details(order_id):
    """Shows details of an order.

    arguments:
    order_id - id of the order

    Requires administrator privileges.
    """
    order = Order.get_by_id(order_id)

    return render_template('order/order_details.html', order=order)


@app.route('/order/add_discount/<int:order_id>', methods=['GET'])
@admin_required
def add_discount(order_id):
    """Activates a discount for an order.

    arguments:
    order_id - id of the order

    Requires administrator privileges.
    """
    flash('Not implemented yet', 'alert-info')
    return redirect(url_for('list_orders'))


@app.route('/order/reject/<int:order_id>', methods=['GET'])
@admin_required
def reject_order(order_id):
    """Rejects an order.

    arguments:
    order_id - id of the order

    Requires administrator privileges.
    """
    o = Order.get_by_id(order_id)
    o.mark_as_rejected()
    return redirect(url_for('list_orders'))


@app.route('/order/deliver/<int:order_id>', methods=['GET', 'POST'])
@admin_required
def mark_order_as_delivered(order_id):
    """Marks an order as delivered.

    arguments:
    order_id - id of the order

    Receives booleans of whether the customer was found and if there were
    any problems with the delivery.

    Requires administrator privileges.
    """
    if request.method == 'POST':
        o = Order.get_by_id(order_id)
        customer_found = request.form['customer_found']
        had_problems = request.form['had_problems']

        o.mark_as_delivered(customer_found, had_problems)

        return redirect(url_for('list_orders'))

    return render_template('order/deliver_order.html')


@app.route('/order/edit/<int:order_id>', methods=['GET', 'POST'])
@admin_required
def edit_order(order_id):
    """Edits an order.

    arguments:
    order_id - id of the order

    Requires administrator privileges.
    """
    return render_template('order/edit_order.html', order=order)


@app.route('/order/delete/<int:order_id>', methods=['GET'])
@admin_required
def delete_order(order_id):
    """Deletes an order.

    arguments:
    order_id - id of the order

    Requires administrator privileges.
    """
    Order.delete_by_id(order_id)

    return redirect(url_for('list_orders'))


@app.route('/order/remove/<string:item_type>/<int:item_id>', methods=['GET'])
@login_required
def remove_item_from_order(item_type, item_id):
    """Removes an item from the order.

    arguments:
    item_type - type of the item as a string (pizza, kebab, drink)
    item_id - id of the item
    """
    if item_type not in ['pizza', 'kebab', 'drink']:
        flash('Unknown item type', 'alert-warning')
        return redirect(url_for('new_order'))

    session_key = 'selected_{}s'.format(item_type)
    new_list = session[session_key]
    new_list.remove(item_id)
    session[session_key] = new_list

    return redirect(url_for('new_order'))


@app.route('/order/set_delivery_address', methods=['POST'])
@login_required
def set_delivery_address():
    """Saves the delivery address to the session.

    Receives the delivery address in POST.
    """
    delivery_address = request.form['delivery_address']

    session['delivery_address'] = delivery_address

    return redirect(url_for('new_order'))
