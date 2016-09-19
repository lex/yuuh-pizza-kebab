import re


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


class Topping():
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price
