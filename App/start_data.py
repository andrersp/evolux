# -*- coding: utf-8 - *-
import string
from random import randint, uniform, choice
from model.numbers import ModelNumber


from model.tables import ModelTable
from model.users import ModelUser

from lorem.text import TextLorem


def create_user():
    data = {
        "id": "1",
        "username": "admin",
        "password": "admin",
        "active": True
    }

    user = ModelUser.find_user(data.get("id"))

    if not user:
        try:
            user = ModelUser(**data)
            user.hash_password()
            user.save_user()
        except Exception as err:
            print(err)


def create_tables_data():

    lorem = TextLorem(srange=(1, 2))
    for i in range(0, 40):

        data = {
            "table_id": i + 1,
            "name": lorem.sentence(),
            "max_line": randint(600, 800)
        }

        table = ModelTable.find_table(data.get("table_id"))

        if not table:
            table = ModelTable(**data)
            table.save_table()


def create_number_data():

    condition = [True, False]
    x = 1
    for _ in range(10):

        for i in range(50):
            values = ''.join(choice(string.digits) for i in range(11))
            data = {
                "id": x,
                "value": "55{}".format(values),
                "monthy_price": round(uniform(0.1, 0.99), 2),
                "setup_price": round(uniform(3.01, 9.99), 2),
                "available": condition[randint(0, 1)],
                "currency": "U$",
                "table_id": randint(1, 40)
            }

            line = ModelNumber.find_number(data.get("id"))

            if not line:
                line = ModelNumber(**data)
                line.save_number()

            x += 1
