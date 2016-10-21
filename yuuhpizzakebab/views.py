from yuuhpizzakebab import app
from flask import render_template


@app.route('/')
def index():
    """Shows the index page."""
    return render_template('index.html', active_tab='home')
