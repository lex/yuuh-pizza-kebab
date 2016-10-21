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
        delivery_summary = get_delivery_summary_for_order(id)

        order = Order(r[0], user, r[2], r[5], r[6], r[7], r[8], r[9],
                      delivery_summary)

        pizzas = get_pizzas_for_order(id)
        kebabs = get_kebabs_for_order(id)
        drinks = get_drinks_for_order(id)

        order.pizzas = pizzas
        order.kebabs = kebabs
        order.drinks = drinks

        return order


def get_delivery_summary_for_order(order_id):
    t = text('select * from DeliverySummary where order_id = :order_id')
    delivery_results = db.engine.execute(t, order_id=order_id)

    if not delivery_results:
        return None

    for r in delivery_results:
        id = int(r[0])
        customer_found = r[1]
        delivered_at = r[2]
        had_problems = r[3]

        return DeliverySummary(id, customer_found, delivered_at, had_problems)


def mark_order_as_delivered(order_id, customer_found, had_problems):
    t = text(
        'insert into DeliverySummary (customer_found, delivered_at, had_problems, order_id) values (:customer_found, now() at time zone \'utc\', :had_problems, :order_id)')
    db.engine.execute(t,
                      order_id=order_id,
                      customer_found=customer_found,
                      had_problems=had_problems)


def mark_order_as_rejected(order_id):
    t = text('update YPKOrder set rejected = \'t\' where id = :order_id')
    db.engine.execute(t, order_id=order_id)


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
    t = text(
        'insert into YPKOrder_Pizza (order_id, pizza_id) values (:order_id, :pizza_id)')
    db.engine.execute(t, order_id=order_id, pizza_id=pizza_id)


def add_kebab_to_order(order_id, kebab_id):
    t = text(
        'insert into YPKOrder_Kebab (order_id, kebab_id) values (:order_id, :kebab_id)')
    db.engine.execute(t, order_id=order_id, kebab_id=kebab_id)


def add_drink_to_order(order_id, drink_id):
    t = text(
        'insert into YPKOrder_Drink (order_id, drink_id) values (:order_id, :drink_id)')
    db.engine.execute(t, order_id=order_id, drink_id=drink_id)


def delete_order(id):
    t = text('delete from YPKOrder where id = :order_id')
    db.engine.execute(t, order_id=id)


def save_order(order):
    ordered_by_id = order.ordered_by.id

    t = text(
        'insert into YPKOrder (ordered_by, delivery_address, delivery_at, lunch_offer_active_when_ordered) values (:ordered_by, :delivery_address, :delivery_at, :lunch_offer_active_when_ordered) returning id')
    result = db.engine.execute(
        t,
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
    """The order class.

    variables:
    id - id of the order
    ordered_by - the user who submitted the order
    ordered_at - timestamp of when the order was created
    delivery_adress - where to deliver the order
    delivery_at - when to deliver the order
    canceled - boolean of whether the order was canceled by the user
    rejected - boolean of whether the order was rejected by an administrator
    lunch_offer_active - boolean of whether the lunch offer was active when the order was placed
    pizzas - list of pizzas included in the order
    kebabs - list of kebabs included in the order
    drinks - list of drinks included in the order
    delivery_summary - information about the possible delivery
    """

    def __init__(self,
                 id,
                 ordered_by,
                 ordered_at,
                 delivery_address,
                 delivery_at,
                 canceled,
                 rejected,
                 lunch_offer_active,
                 delivery_summary=None):
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

        self.delivery_summary = delivery_summary

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

        filtered_orders = []

        for o in orders:
            if not o.rejected and not o.delivery_summary:
                filtered_orders.append(o)

        return filtered_orders

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
            print 'can\'t add kebab without own id'

        add_kebab_to_order(self.id, kebab.id)

    def add_pizza(self, pizza):
        if not self.id:
            print 'can\'t add pizza without own id'

        add_pizza_to_order(self.id, pizza.id)

    def add_drink(self, drink):
        if not self.id:
            print 'can\'t add drink without own id'

        add_drink_to_order(self.id, drink.id)

    def mark_as_delivered(self, customer_found, had_problems):
        if not self.id:
            print 'rip'

        mark_order_as_delivered(self.id, customer_found, had_problems)

    def mark_as_rejected(self):
        if not self.id:
            print 'rip'

        mark_order_as_rejected(self.id)


class DeliverySummary():
    """The delivery summary class.

    Included in a delivered order.

    variables:
    id - id of the order
    customer_found - boolean of whether the customer was found
    delivered_at - timestamp of when the order was delivered
    had_problems - boolean of whether there were problems with the delivery
    """

    def __init__(self, id, customer_found, delivered_at, had_problems):
        self.id = id
        self.customer_found = customer_found
        self.delivered_at = delivered_at
        self.had_problems = had_problems
