# -*- coding: utf-8 -*-

from db import db


class ModelTable(db.Model):
    __tablename__ = 'table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    max_line = db.Column(db.Integer)
    free_lines = db.relationship("ModelNumber")

    __mapper_args__ = {
        'order_by': id
    }

    def __init__(self, table_id, name, max_line):
        self.table_id = table_id
        self.name = name
        self.max_line = max_line

    def list_json(self):
        return {
            "table_id": self.id,
            "name": self.name,
            "max_line": self.max_line,
            "free_lines": len([free.list_json() for free in self.free_lines if free.available]),

        }

    def table_json(self):
        return {
            "table_id": self.id,
            "name": self.name,
            "max_line": self.max_line,
            "free_lines": len([free.list_json() for free in self.free_lines if free.available]),
            "lines": [free.list_json() for free in self.free_lines]
        }

    def save_table(self):
        db.session.add(self)
        db.session.commit()

    def update_table(self, table_id, name, max_line):
        self.name = name
        self.max_line = max_line

    @classmethod
    def find_table(cls, table_id):

        if not table_id:
            return None

        table = cls.query.filter_by(id=table_id).first()

        if table:
            return table

        return None

    def delete_table(self):
        [number.delete_number() for number in self.free_lines]
        db.session.delete(self)
        db.session.commit()
