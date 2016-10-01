from yuuhpizzakebab import app, admin_required, login_required
from .models import Order
from yuuhpizzakebab.user.database_functions import get_user_by_id
from flask import render_template, session, redirect, url_for, request, flash
import datetime


@app.route('/orders')
@admin_required
def list_orders():
    return render_template('order/orders.html', orders=Order.get_all())


@app.route('/orders/active')
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
    flash('Not implemented yet', 'alert-info')
    return redirect(url_for('list_orders'))


@app.route('/order/deliver/<int:order_id>', methods=['GET'])
@admin_required
def mark_order_as_delivered(order_id):
    flash('Not implemented yet', 'alert-info')
    return redirect(url_for('list_orders'))


@app.route('/order/create', methods=['GET', 'POST'])
@admin_required
def create_order():
    if request.method == 'POST':
        delivery_address = request.form['delivery_address']
        delivery_at = int(request.form['delivery_at'])
        delivery_at = datetime.datetime.utcnow() + datetime.timedelta(
            hours=delivery_at)

        user_id = session.get('user_id')
        user = get_user_by_id(user_id)

        o = Order(None, user, None, delivery_address, delivery_at, False,
                  False, False)
        success = o.save()

        if not success:
            flash('Some fields need to be filled', 'alert-danger')
            return render_template('order/edit_order.html', order=o)

        flash('Created order', 'alert-success')
        return redirect(url_for('list_orders'))

    return render_template('order/edit_order.html')


@app.route('/order/edit/<int:order_id>', methods=['GET', 'POST'])
@admin_required
def edit_order(order_id):
    if request.method == 'POST':
        name = request.form['order_name']
        price = request.form['order_price']
        image_url = request.form['order_image_url']

        o = Order(order_id, name, price, image_url)
        o.save()

        return redirect(url_for('list_orders'))

    order = Order.get_by_id(order_id)

    if not order:
        return redirect(url_for('list_orders'))

    return render_template('order/edit_order.html', order=order)


@app.route('/order/delete/<int:order_id>')
@admin_required
def delete_order(order_id):
    Order.delete_by_id(order_id)

    return redirect(url_for('list_orders'))
