from sqlalchemy import text
from yuuhpizzakebab import db
from yuuhpizzakebab.pizza.models import Pizza, Topping


def get_pizzas():
    result = db.engine.execute('select * from Pizza')
    pizzas = []

    for r in result:
        pizza_id = int(r[0])
        toppings = []

        t = text(
            'select * from Topping where id in (select topping_id from Pizza_Topping where pizza_id = :pizza_id)')
        toppings_results = db.engine.execute(t, pizza_id=pizza_id)

        for t in toppings_results:
            toppings.append(Topping(t[0], t[1], t[2]))

        pizzas.append(Pizza(r[0], r[1], r[2], toppings))

    return pizzas
