from yuuhpizzakebab import app, admin_required, login_required
from .models import Kebab
from flask import render_template, session, redirect, url_for, request


@app.route('/kebabs')
def list_kebabs():
    return render_template('kebab/kebabs.html', kebabs=Kebab.get_all())


@app.route('/kebab/create', methods=['GET', 'POST'])
@admin_required
def create_kebab():
    if request.method == 'POST':
        name = request.form['kebab_name']
        price = request.form['kebab_price']
        image_url = request.form['kebab_image_url']

        k = Kebab(None, name, price, image_url)
        k.save()

        return redirect(url_for('list_kebabs'))

    return render_template('kebab/create_kebab.html')


@app.route('/kebab/edit/<int:kebab_id>', methods=['GET', 'POST'])
@admin_required
def edit_kebab(kebab_id):
    if request.method == 'POST':
        name = request.form['kebab_name']
        price = request.form['kebab_price']
        image_url = request.form['kebab_image_url']

        k = Kebab(kebab_id, name, price, image_url)
        k.save()

        return redirect(url_for('list_kebabs'))

    kebab = Kebab.get_by_id(kebab_id)

    if not kebab:
        return redirect(url_for('list_kebabs'))

    return render_template('kebab/edit_kebab.html', kebab=kebab)


@app.route('/kebab/delete/<int:kebab_id>')
@admin_required
def delete_kebab(kebab_id):
    Kebab.delete_by_id(kebab_id)

    return redirect(url_for('list_kebabs'))
