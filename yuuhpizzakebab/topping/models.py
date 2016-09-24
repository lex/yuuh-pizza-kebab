from sqlalchemy import text
from yuuhpizzakebab import db


def get_toppings():
    result = db.engine.execute('select * from Topping')
    toppings = []

    for r in result:
        toppings.append(Topping(r[0], r[1], r[2]))

    return toppings


def get_topping(id):
    t = text('select * from Topping where id = :topping_id')
    topping_results = db.engine.execute(t, topping_id=id)

    if not topping_results:
        return None

    for r in topping_results:
        return Topping(r[0], r[1], r[2])


def delete_topping(id):
    t = text('delete from Topping where id = :topping_id')
    db.engine.execute(t, topping_id=id)


def save_topping(topping):
    t = text('insert into Topping (name, price) values (:name, :price)')
    db.engine.execute(t, name=topping.name, price=topping.price)


def update_topping(topping):
    t = text(
        'update Topping set name = :name, price = :price where id = :topping_id')
    db.engine.execute(t,
                      name=topping.name,
                      price=topping.price,
                      topping_id=topping.id)


class Topping():
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    @staticmethod
    def get_all():
        return get_toppings()

    def price_without_dollar_sign(self):
        return str(self.price)[1:]

    @staticmethod
    def get_by_id(id):
        return get_topping(id)

    def save(self):
        if self.id:
            update_topping(self)
            return

        save_topping(self)

    @staticmethod
    def delete_by_id(id):
        delete_topping(id)

    def delete(self):
        if not self.id:
            print 'can\'t delete without id t: topping'
            return

        delete_topping(self.id)
