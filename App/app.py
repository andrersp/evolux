# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from view.tables import get_tables, save_table, get_table, delete_table
from view.numbers import get_numbers, save_number, get_number, delete_number
from view.user import get_users, get_user, save_user, user_login

from db import db
from start_data import create_user, create_tables_data, create_number_data

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://evolux:evolux@db/evolux"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = 'evoluxjob'
db.init_app(app)
bcript = Bcrypt(app)
jwt = JWTManager(app)


# 404 Error
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "URL not Found"}), 404


@app.before_first_request
def create_tables():
    db.create_all()
    create_user()
    create_tables_data()
    create_number_data()


@app.route("/", methods=["GET"])
def home():
    return jsonify({"Message": "Sucess"}), 200


@app.route("/tables", methods=["GET"])
def route_get_tables():
    return get_tables()


@app.route("/table", methods=["POST"])
def route_save_table():
    return save_table()


@app.route("/table/<int:table_id>", methods=["GET"])
def route_get_table(table_id):
    return get_table(table_id)


@app.route("/table/<int:table_id>", methods=["DELETE"])
def route_delete_table(table_id):
    return delete_table(table_id)


@app.route("/numbers", methods=["GET"])
def route_get_numbers():
    return get_numbers()


@app.route("/number", methods=["POST"])
def route_save_number():
    return save_number()


@app.route("/number/<int:number_id>", methods=["GET"])
def route_get_number(number_id):
    return get_number(number_id)


@app.route("/number/<int:number_id>", methods=["DELETE"])
def route_delete_number(number_id):
    return delete_number(number_id)


@app.route("/users", methods=["GET"])
def route_get_users():
    return get_users()


@app.route("/user/<int:id_user>", methods=["GET"])
def route_get_user(id_user):
    return get_user(id_user)


@app.route("/user", methods=["POST"])
def route_save_user():
    return save_user()


@app.route("/login", methods=["POST"])
def route_login():
    return user_login()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
