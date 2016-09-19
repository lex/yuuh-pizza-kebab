# Yuuh Pizza Kebab
Yuuh Pizza Kebab is a pizza ordering service.
# Usage
```
$ git clone https://github.com/lex/yuuh-pizza-kebab
$ cd yuuh-pizza-kebab
$ virtualenv venv
$ . venv/bin/activate
(venv) $ pip install -r requirements.txt

(venv) $ export SECRET_KEY='verysecret'
(venv) $ export DATABASE_URL='postgres://username:password@127.0.0.1:5432/database_name'

optional:
(venv) $ export DEBUG=juuh

(venv) $ heroku local
or
(venv) $ python app.py

$ curl 127.0.0.1:5000
kebab coming soon
$ 
```
##### Good To Know
- [Live demo](http://yuuh-pizza-service.herokuapp.com)
    - Username: yuuh
    - Password: yuuh
- [Documentation](doc/documentation.pdf)
- [Subject](http://advancedkittenry.github.io/suunnittelu_ja_tyoymparisto/aiheet/Pizzapalvelu.html)

