from sqlalchemy import text
from yuuhpizzakebab import db
from yuuhpizzakebab.kebab.models import Kebab


def get_kebabs():
    result = db.engine.execute('select * from Kebab')
    kebabs = []

    for r in result:
        kebabs.append(Kebab(r[0], r[1], r[2]))

    return kebabs
