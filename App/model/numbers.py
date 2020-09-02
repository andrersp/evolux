# -*- coding: utf-8 -*-

from db import db


class ModelNumber(db.Model):
    __tablename__ = "did_number"
    number_id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(20))
    monthy_price = db.Column(db.Float(precision=2))
    setup_price = db.Column(db.Float(precision=2))
    currency = db.Column(db.String(4))
    available = db.Column(db.Boolean)
    table_id = db.Column(db.Integer, db.ForeignKey("table.id"))
    table_name = db.relationship(
        "ModelTable", foreign_keys="ModelNumber.table_id")

    def __init__(self, id, value, monthy_price, setup_price,
                 currency, available, table_id):
        self.id = id
        self.value = value
        self.monthy_price = monthy_price
        self.setup_price = setup_price
        self.currency = currency
        self.available = available
        self.table_id = table_id

    def list_json(self):
        return {
            "id": self.number_id,
            "value": "+{} {} {}-{}".format(self.value[:2], self.value[2:4], self.value[4:9], self.value[9:]),
            "monthyPrice": "{:.2f}".format(self.monthy_price),
            "setupPrice": "{:.2f}".format(self.setup_price),
            "currency": self.currency,
            "available": self.available,

        }

    def number_json(self):
        return {
            "id": self.number_id,
            "value": "+{} {} {}-{}".format(self.value[:2], self.value[2:4], self.value[4:9], self.value[9:]),
            "monthyPrice": "{:.2f}".format(self.monthy_price),
            "setupPrice": "{:.2f}".format(self.setup_price),
            "currency": self.currency,
            "available": self.available,
            "table_id": self.table_id if self.table_id else "",
            "table_name": self.table_name.name if self.table_name else ""

        }

    def save_number(self):
        db.session.add(self)
        db.session.commit()

    def delete_number(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_number(cls, number_id):
        if not number_id:
            return None

        number = cls.query.filter_by(number_id=number_id).first()

        if number:
            return number

        return None

    def update_number(self, id, value, monthy_price, setup_price,
                      currency, available, table_id):
        self.value = value
        self.monthy_price = monthy_price
        self.setup_price = setup_price
        self.currency = currency
        self.available = available
        self.table_id = table_id
