import re

from sqlalchemy import text
from yuuhpizzakebab import db


def get_pizzas():
    result = db.engine.execute('select * from Pizza')
    pizzas = []

    for r in result:
        pizza_id = int(r[0])
        toppings = get_toppings(pizza_id)

        pizzas.append(Pizza(r[0], r[1], r[2], r[3], toppings))

    return pizzas


def get_toppings(pizza_id):
    toppings = []

    t = text(
        'select * from Topping where id in (select topping_id from Pizza_Topping where pizza_id = :pizza_id)')
    topping_results = db.engine.execute(t, pizza_id=pizza_id)

    for t in topping_results:
        toppings.append(Topping(t[0], t[1], t[2]))

    return toppings


def get_pizza(id):
    t = text('select * from Pizza where id = :pizza_id')
    pizza_results = db.engine.execute(t, pizza_id=id)

    if not pizza_results:
        return None

    for r in pizza_results:
        pizza_id = int(r[0])
        toppings = get_toppings(pizza_id)
        return Pizza(r[0], r[1], r[2], r[3], toppings)


def delete_pizza(id):
    delete_toppings_for_pizza(id)
    t = text('delete from Pizza where id = :pizza_id')
    db.engine.execute(t, pizza_id=id)


def delete_toppings_for_pizza(pizza_id):
    t = text('delete from Pizza_Topping where pizza_id = :pizza__id')
    db.engine.execute(t, pizza__id=pizza_id)


def save_pizza(pizza):
    t = text(
        'insert into Pizza (name, price, image_url) values (:name, :price, :image__url)')
    db.engine.execute(t,
                      name=pizza.name,
                      price=pizza.price,
                      image__url=pizza.image_url)


def update_pizza(pizza):
    t = text(
        'update Pizza set name = :name, price = :price, image_url = :image__url where id = :pizza_id')
    db.engine.execute(t,
                      name=pizza.name,
                      price=pizza.price,
                      image__url=pizza.image_url,
                      pizza_id=pizza.id)


class Pizza():
    def __init__(self, id, name, price, image_url, toppings):
        self.id = id
        self.name = name
        self.price = price
        self.image_url = image_url
        self.toppings = toppings

    def toppings_as_string(self):
        if not self.toppings:
            return '-'

        s = ''
        for t in self.toppings:
            s += t.name
            s += ', '

        s = re.sub(', $', '', s)
        return s

    def price_without_dollar_sign(self):
        return str(self.price)[1:]

    @staticmethod
    def get_all():
        return get_pizzas()

    @staticmethod
    def get_by_id(id):
        return get_pizza(id)

    def save(self):
        if self.id:
            update_pizza(self)
            return

        save_pizza(self)

    @staticmethod
    def delete_by_id(id):
        delete_pizza(id)

    def delete(self):
        if not self.id:
            print 'can\'t delete without id t: pizza'
            return

        delete_pizza(self.id)


class Topping():
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price
