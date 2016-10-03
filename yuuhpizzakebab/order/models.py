from sqlalchemy import text
from yuuhpizzakebab import db
from yuuhpizzakebab.user.database_functions import get_user_by_id
from yuuhpizzakebab.pizza.models import Pizza
from yuuhpizzakebab.kebab.models import Kebab
from yuuhpizzakebab.drink.models import Drink


def get_orders():
    result = db.engine.execute('select id from YPKOrder')
    orders = []

    for r in result:
        order_id = int(r[0])
        orders.append(get_order(order_id))

    return orders


def get_order(id):
    t = text('select * from YPKOrder where id = :order_id')
    order_results = db.engine.execute(t, order_id=id)

    if not order_results:
        return None

    for r in order_results:
        user_id = int(r[1])
        user = get_user_by_id(user_id)

        order = Order(r[0], user, r[2], r[5], r[6], r[7], r[8], r[9])

        pizzas = get_pizzas_for_order(id)
        kebabs = get_kebabs_for_order(id)
        drinks = get_drinks_for_order(id)

        order.pizzas = pizzas
        order.kebabs = kebabs
        order.drinks = drinks

        return order


def get_pizzas_for_order(order_id):
    t = text('select pizza_id from YPKOrder_Pizza where order_id = :order_id')
    results = db.engine.execute(t, order_id=order_id)

    pizzas = []

    for r in results:
        pizza_id = int(r[0])
        pizzas.append(Pizza.get_by_id(pizza_id))

    return pizzas


def get_kebabs_for_order(order_id):
    t = text('select kebab_id from YPKOrder_Kebab where order_id = :order_id')
    results = db.engine.execute(t, order_id=order_id)

    kebabs = []

    for r in results:
        kebab_id = int(r[0])
        kebabs.append(Kebab.get_by_id(kebab_id))

    return kebabs


def get_drinks_for_order(order_id):
    t = text('select drink_id from YPKOrder_Drink where order_id = :order_id')
    results = db.engine.execute(t, order_id=order_id)

    drinks = []

    for r in results:
        drink_id = int(r[0])
        drinks.append(Drink.get_by_id(drink_id))

    return drinks

def add_pizza_to_order(order_id, pizza_id):
    t = text('insert into YPKOrder_Pizza (order_id, pizza_id) values (:order_id, :pizza_id)')
    db.engine.execute(t, order_id=order_id, pizza_id=pizza_id)

def add_kebab_to_order(order_id, kebab_id):
    t = text('insert into YPKOrder_Kebab (order_id, kebab_id) values (:order_id, :kebab_id)')
    db.engine.execute(t, order_id=order_id, kebab_id=kebab_id)

def add_drink_to_order(order_id, drink_id):
    t = text('insert into YPKOrder_Drink (order_id, drink_id) values (:order_id, :drink_id)')
    db.engine.execute(t, order_id=order_id, drink_id=drink_id)


def delete_order(id):
    t = text('delete from YPKOrder where id = :order_id')
    db.engine.execute(t, order_id=id)


def save_order(order):
    ordered_by_id = order.ordered_by.id

    t = text(
        'insert into YPKOrder (ordered_by, delivery_address, delivery_at, lunch_offer_active_when_ordered) values (:ordered_by, :delivery_address, :delivery_at, :lunch_offer_active_when_ordered) returning id')
    result = db.engine.execute(t,
                      ordered_by=ordered_by_id,
                      delivery_address=order.delivery_address,
                      delivery_at=order.delivery_at,
                      lunch_offer_active_when_ordered=order.lunch_offer_active)

    for r in result:
        order.id = int(r[0])
        return


def update_order(order):
    pass


class Order():
    def __init__(self, id, ordered_by, ordered_at, delivery_address,
                 delivery_at, canceled, rejected, lunch_offer_active):
        self.id = id
        self.ordered_by = ordered_by
        self.ordered_at = ordered_at
        self.delivery_address = delivery_address
        self.delivery_at = delivery_at
        self.canceled = canceled
        self.rejected = rejected
        self.lunch_offer_active = lunch_offer_active

        self.pizzas = []
        self.kebabs = []
        self.drinks = []

    def total_price(self):
        total = 0.0

        for p in self.pizzas:
            total += float(p.price_without_dollar_sign())

        for k in self.kebabs:
            total += float(k.price_without_dollar_sign())

        for d in self.drinks:
            total += float(d.price_without_dollar_sign())

        return total

    @staticmethod
    def get_all():
        return get_orders()

    @staticmethod
    def get_all_active():
        orders = get_orders()

        # filter here or in the database
        print('fix fix fix fix')

        return orders

    @staticmethod
    def get_by_id(id):
        return get_order(id)

    def save(self):
        if self.id:
            update_order(self)
            return True

        save_order(self)

        return True

    @staticmethod
    def delete_by_id(id):
        delete_order(id)

    def delete(self):
        if not self.id:
            print 'can\'t delete without id t: order'
            return False

        delete_order(self.id)

        return True

    def add_kebab(self, kebab):
        if not self.id:
            print('can\'t add kebab without own id')

        add_kebab_to_order(self.id, kebab.id)

    def add_pizza(self, pizza):
        if not self.id:
            print('can\'t add pizza without own id')

        add_pizza_to_order(self.id, pizza.id)

    def add_drink(self, drink):
        if not self.id:
            print('can\'t add drink without own id')

        add_drink_to_order(self.id, drink.id)




