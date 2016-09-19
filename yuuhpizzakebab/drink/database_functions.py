from sqlalchemy import text
from yuuhpizzakebab import db
from yuuhpizzakebab.drink.models import Drink


def get_drinks():
    result = db.engine.execute('select * from Drink')
    drinks = []

    for r in result:
        drinks.append(Drink(r[0], r[1], r[2], r[3]))

    return drinks
