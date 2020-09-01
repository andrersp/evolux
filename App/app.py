# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from view.tables import get_tables, save_table, get_table, delete_table
from view.numbers import get_numbers, save_number, get_number, delete_number

from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://evolux:evolux@db/evolux"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
