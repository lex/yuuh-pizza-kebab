from yuuhpizzakebab import app
from yuuhpizzakebab.kebab.models import Kebab
from flask import render_template, session, redirect, url_for, request


@app.route('/kebabs')
def list_kebabs():
    return render_template('kebabs.html',
                           active_tab='kebabs',
                           kebabs=Kebab.get_all())


@app.route('/kebab_test')
def kebab_test():
    k = Kebab(None, 'juuh', 120.15, 'rip')
    k.save()

    return redirect(url_for('list_kebabs'))


@app.route('/kebab/create', methods=['POST'])
def create_kebab():
    name = request.form['kebab_name']
    price = request.form['kebab_price']
    image_url = request.form['kebab_image_url']

    k = Kebab(None, name, price, image_url)
    k.save()

    return redirect(url_for('list_kebabs'))


@app.route('/kebab/delete/<int:kebab_id>')
def delete_kebab(kebab_id):
    Kebab.delete_by_id(kebab_id)

    return redirect(url_for('list_kebabs'))
