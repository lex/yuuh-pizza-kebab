import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

@app.route('/')
def kebab():
    return 'kebab coming soon'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
