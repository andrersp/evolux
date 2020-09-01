# -*- coding: utf-8 -*-

from flask_bcrypt import generate_password_hash, check_password_hash

from db import db


class ModelUser(db.Model):
    __tablename_ = "user"
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(80))
    active = db.Column(db.Boolean, default=True)

    __mapper_args__ = {
        "order_by": id_user
    }

    def __init__(self, id, username, password, active):
        self.id = id
        self.username = username
        self.password = password
        self.active = active

    def user_json(self):
        return {
            "id": self.id_user,
            "username": self.username,
            "password": self.password,
            "active": self.active
        }

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password):

        return check_password_hash(self.password, password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    def update_user(self, id, username, password, active):
        self.username = username
        self.password = password
        self.active = active

    @classmethod
    def find_username(cls, username):

        if not username:
            return None

        username = cls.query.filter_by(username=username).first()

        if username:
            return username
        return None

    @classmethod
    def find_user(cls, id_user):

        if not id_user:
            return None

        user = cls.query.filter_by(id_user=id_user).first()

        if user:
            return user
        return None
