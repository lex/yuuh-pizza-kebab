from sqlalchemy import text
from yuuhpizzakebab import db

def get_drinks():
    result = db.engine.execute('select * from Drink')
    drinks = []

    for r in result:
        drinks.append(Drink(r[0], r[1], r[2], r[3]))

    return drinks


def get_drink(id):
    t = text('select * from Drink where id = :drink_id')
    drink_results = db.engine.execute(t, drink_id=id)

    if not drink_results:
        return None

    for r in drink_results:
        return Drink(r[0], r[1], r[2], r[3])


def delete_drink(id):
    t = text('delete from Drink where id = :drink_id')
    db.engine.execute(t, drink_id=id)


def save_drink(drink):
    t = text(
        'insert into Drink (name, price, image_url) values (:name, :price, :image__url)')
    db.engine.execute(t,
                      name=drink.name,
                      price=drink.price,
                      image__url=drink.image_url)


def update_drink(drink):
    t = text(
        'update Drink set name = :name, price = :price, image_url = :image__url where id = :drink_id')
    db.engine.execute(t,
                      name=drink.name,
                      price=drink.price,
                      image__url=drink.image_url,
                      drink_id=drink.id)

class Drink():
    def __init__(self, id, name, price, image_url):
        self.id = id
        self.name = name
        self.price = price
        self.image_url = image_url

    def price_without_dollar_sign(self):
        return str(self.price)[1:]

    @staticmethod
    def get_all():
        return get_drinks()

    @staticmethod
    def get_by_id(id):
        return get_drink(id)

    def save(self):
        if not self.name:
            return False
        if not self.price:
            return False
        if not self.image_url:
            return False

        if self.id:
            update_drink(self)
            return True

        save_drink(self)

        return True

    @staticmethod
    def delete_by_id(id):
        delete_drink(id)

    def delete(self):
        if not self.id:
            print 'can\'t delete without id t: drink'
            return False

        delete_drink(self.id)

        return True
