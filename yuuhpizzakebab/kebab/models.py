from sqlalchemy import text
from yuuhpizzakebab import db


def get_kebabs():
    result = db.engine.execute('select * from Kebab')
    kebabs = []

    for r in result:
        kebabs.append(Kebab(r[0], r[1], r[2], r[3]))

    return kebabs


def get_kebab(id):
    t = text('select * from Kebab where id = :kebab_id')
    kebab_results = db.engine.execute(t, kebab_id=id)

    if not kebab_results:
        return None

    for r in kebab_results:
        return Kebab(r[0], r[1], r[2], r[3])


def delete_kebab(id):
    t = text('delete from Kebab where id = :kebab_id')
    db.engine.execute(t, kebab_id=id)


def save_kebab(kebab):
    t = text(
        'insert into Kebab (name, price, image_url) values (:name, :price, :image__url)')
    db.engine.execute(t,
                      name=kebab.name,
                      price=kebab.price,
                      image__url=kebab.image_url)


def update_kebab(kebab):
    t = text(
        'update Kebab set name = :name, price = :price, image_url = :image__url where id = :kebab_id')
    db.engine.execute(t,
                      name=kebab.name,
                      price=kebab.price,
                      image__url=kebab.image_url,
                      kebab_id=kebab.id)


class Kebab():
    def __init__(self, id, name, price, image_url):
        self.id = id
        self.name = name
        self.price = price
        self.image_url = image_url

    def price_without_dollar_sign(self):
        return str(self.price)[1:]

    @staticmethod
    def get_all():
        return get_kebabs()

    @staticmethod
    def get_by_id(id):
        return get_kebab(id)

    def save(self):
        if not self.name:
            return False
        if not self.price:
            return False
        if not self.image_url:
            return False

        if self.id:
            update_kebab(self)
            return True

        save_kebab(self)

        return True

    @staticmethod
    def delete_by_id(id):
        delete_kebab(id)

    def delete(self):
        if not self.id:
            print 'can\'t delete without id t: kebab'
            return False

        delete_kebab(self.id)

        return True
