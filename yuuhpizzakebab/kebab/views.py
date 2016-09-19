from yuuhpizzakebab import app
from yuuhpizzakebab.kebab.database_functions import get_kebabs
from flask import render_template


@app.route('/kebabs')
def list_kebabs():
    return render_template('kebabs.html',
                           active_tab='kebabs',
                           kebabs=get_kebabs())
