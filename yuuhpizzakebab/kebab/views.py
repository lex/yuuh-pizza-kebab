from yuuhpizzakebab import app, admin_required, login_required
from .models import Kebab
from flask import render_template, session, redirect, url_for, request, flash


@app.route('/kebabs', methods=['GET'])
def list_kebabs():
    """Shows a list of kebabs."""
    return render_template('kebab/kebabs.html',
                           kebabs=Kebab.get_all(),
                           selecting=request.args.get('selecting'))


@app.route('/kebab/create', methods=['GET'])
@admin_required
def create_kebab():
    """Creates a new kebabs.

    Creates a new kebab with POST.
    Shows a form to fill with GET.
    """
    if request.method == 'POST':
        name = request.form['kebab_name']
        price = request.form['kebab_price']
        image_url = request.form['kebab_image_url']

        k = Kebab(None, name, price, image_url)
        success = k.save()

        if not success:
            flash('Some fields need to be filled', 'alert-danger')
            return render_template('kebab/edit_kebab.html', kebab=k)

        flash('Created kebab', 'alert-success')
        return redirect(url_for('list_kebabs'))

    return render_template('kebab/edit_kebab.html')


@app.route('/kebab/edit/<int:kebab_id>', methods=['GET', 'POST'])
@admin_required
def edit_kebab(kebab_id):
    """Edits a kebabs.

    arguments:
    kebab_id -- id of the kebab

    Saves the information with POST.
    Shows a form to edit the contents with GET.
    """
    if request.method == 'POST':
        name = request.form['kebab_name']
        price = request.form['kebab_price']
        image_url = request.form['kebab_image_url']

        k = Kebab(kebab_id, name, price, image_url)
        success = k.save()

        if not success:
            flash('Some fields need to be filled', 'alert-danger')
            return render_template('kebab/edit_kebab.html', kebab=k)

        return redirect(url_for('list_kebabs'))

    kebab = Kebab.get_by_id(kebab_id)

    if not kebab:
        flash('Couldn\'t find such kebab', 'alert-warning')
        return redirect(url_for('list_kebabs'))

    return render_template('kebab/edit_kebab.html', kebab=kebab)


@app.route('/kebab/delete/<int:kebab_id>', methods=['GET'])
@admin_required
def delete_kebab(kebab_id):
    """Deletes a kebab.

    arguments:
    kebab_id -- id of the kebab
    """
    Kebab.delete_by_id(kebab_id)
    flash('Removed kebab', 'alert-success')

    return redirect(url_for('list_kebabs'))
