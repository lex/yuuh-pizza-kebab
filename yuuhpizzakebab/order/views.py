from yuuhpizzakebab import app, admin_required, login_required
from .models import Order
from yuuhpizzakebab.pizza.models import Pizza
from yuuhpizzakebab.kebab.models import Kebab
from yuuhpizzakebab.drink.models import Drink
from yuuhpizzakebab.user.database_functions import get_user_by_id
from flask import render_template, session, redirect, url_for, request, flash
import datetime


def get_pizzas_from_session():
    pizzas = []

    if session.get('selected_pizzas'):
        for pizza_id in session.get('selected_pizzas'):
            p = Pizza.get_by_id(pizza_id)
            pizzas.append(p)

    return pizzas


def get_kebabs_from_session():
    kebabs = []

    if session.get('selected_kebabs'):
        for kebab_id in session['selected_kebabs']:
            k = Kebab.get_by_id(kebab_id)
            kebabs.append(k)

    return kebabs


def get_drinks_from_session():
    drinks = []

    if session.get('selected_drinks'):
        for drink_id in session['selected_drinks']:
            d = Drink.get_by_id(drink_id)
            drinks.append(d)

    return drinks


def get_total_price_of_items(pizzas, kebabs, drinks):
    total = 0.0

    for p in pizzas:
        total += float(p.price_without_dollar_sign())

    for k in kebabs:
        total += float(k.price_without_dollar_sign())

    for d in drinks:
        total += float(d.price_without_dollar_sign())

    return total


def get_delivery_address():
    return session.get('delivery_address')


def clear_session():
    session.pop('selected_pizzas', None)
    session.pop('selected_kebabs', None)
    session.pop('selected_drinks', None)


@app.route('/new_order', methods=['GET'])
@login_required
def new_order():
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
    if item_type not in ['pizza', 'kebab', 'drink']:
        flash('Unknown item type', 'alert-warning')
        return redirect(url_for('new_order'))

    return redirect(url_for('list_{}s'.format(item_type), selecting=True))


@app.route('/select/pizza/<int:pizza_id>', methods=['GET'])
@login_required
def select_pizza(pizza_id):
    if not session.get('selected_pizzas'):
        session['selected_pizzas'] = []

    new_list = session['selected_pizzas']
    new_list.append(pizza_id)
    session['selected_pizzas'] = new_list

    return redirect(url_for('new_order'))


@app.route('/select/kebab/<int:kebab_id>', methods=['GET'])
@login_required
def select_kebab(kebab_id):
    if not session.get('selected_kebabs'):
        session['selected_kebabs'] = []

    new_list = session['selected_kebabs']
    new_list.append(kebab_id)
    session['selected_kebabs'] = new_list

    return redirect(url_for('new_order'))


@app.route('/select/drink/<int:drink_id>', methods=['GET'])
@login_required
def select_drink(drink_id):
    if not session.get('selected_drinks'):
        session['selected_drinks'] = []

    new_list = session['selected_drinks']
    new_list.append(drink_id)
    session['selected_drinks'] = new_list

    return redirect(url_for('new_order'))


@app.route('/place_order', methods=['GET'])
@login_required
def place_order():
    pizzas = get_pizzas_from_session()
    kebabs = get_kebabs_from_session()
    drinks = get_drinks_from_session()
    total_price = get_total_price_of_items(pizzas, kebabs, drinks)

    user_id = session['user_id']
    user = get_user_by_id(user_id)
    ordered_at = datetime.datetime.utcnow()
    delivery_address = get_delivery_address()
    delivery_at = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
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
    clear_session()
    return redirect(url_for('new_order'))


@app.route('/orders', methods=['GET'])
@admin_required
def list_orders():
    return render_template('order/orders.html', orders=Order.get_all())


@app.route('/orders/active', methods=['GET'])
@admin_required
def list_active_orders():
    return render_template('order/orders.html', orders=Order.get_all_active())


@app.route('/order/<int:order_id>', methods=['GET'])
@admin_required
def order_details(order_id):
    order = Order.get_by_id(order_id)

    return render_template('order/order_details.html', order=order)


@app.route('/order/add_discount/<int:order_id>', methods=['GET'])
@admin_required
def add_discount(order_id):
    flash('Not implemented yet', 'alert-info')
    return redirect(url_for('list_orders'))


@app.route('/order/reject/<int:order_id>', methods=['GET'])
@admin_required
def reject_order(order_id):
    o = Order.get_by_id(order_id)
    o.mark_as_rejected()
    return redirect(url_for('list_orders'))


@app.route('/order/deliver/<int:order_id>', methods=['GET', 'POST'])
@admin_required
def mark_order_as_delivered(order_id):
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
    return render_template('order/edit_order.html', order=order)


@app.route('/order/delete/<int:order_id>', methods=['GET'])
@admin_required
def delete_order(order_id):
    Order.delete_by_id(order_id)

    return redirect(url_for('list_orders'))


@app.route('/order/remove/<string:item_type>/<int:item_id>', methods=['GET'])
@login_required
def remove_item_from_order(item_type, item_id):
    session_key = 'selected_{}s'.format(item_type)
    new_list = session[session_key]
    new_list.remove(item_id)
    session[session_key] = new_list

    return redirect(url_for('new_order'))


@app.route('/order/set_delivery_address', methods=['POST'])
@login_required
def set_delivery_address():
    delivery_address = request.form['delivery_address']

    session['delivery_address'] = delivery_address

    return redirect(url_for('new_order'))
