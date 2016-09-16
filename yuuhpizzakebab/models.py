import re


class Pizza():
    def __init__(self, id, name, price, toppings):
        self.id = id
        self.name = name
        self.price = price
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

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'toppings': [t.serialize() for t in self.toppings],
        }


class Topping():
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def serialize(self):
        return {'id': self.id, 'name': self.name, 'price': self.price, }


class Kebab():
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price


class User():
    def __init__(self, id, username, is_admin):
        self.id = id
        self.username = username
        self.is_admin = is_admin
