# -*- coding: utf-8 -*-

from flask import jsonify, request, make_response

from wraps import required_params

from model.numbers import ModelNumber
from model.tables import ModelTable


schema = {
    "id": {"required": True, "nullable": True},
    "value": {"required": True, "type": "string"},
    "monthy_price": {"required": True, "type": "float"},
    "setup_price": {"required": True, "type": "float"},
    "currency": {"required": True, "type": "string"},
    "available": {"required": True, "type": "boolean"},
    "table_id": {"required": True, "type": "integer"}
}


def get_numbers():
    data = [number.list_json() for number in ModelNumber.query.all()]
    respose = make_response(jsonify({"data": data}), 200)
    return respose


@required_params(schema)
def save_number():

    data = request.json

    table = ModelTable.find_table(data.get("table_id"))

    if not table:
        return make_response(jsonify({"message": "table_id does not match ", "data": {}}), 400)

    number = ModelNumber.find_number(data.get("id"))

    if number:
        return update_number()

    try:
        number = ModelNumber(**data)

        number.save_number()

        return make_response(jsonify({"message": "New Number Saved", "data": number.number_json()}), 201)
    except:
        return make_response(jsonify({"message": "Internal Error", "data": {}}), 500)


@required_params(schema)
def update_number():

    data = request.json

    number = ModelNumber.find_number(data.get("id"))

    if not number:
        return make_response(jsonify({"message": "Number not found", "data": {}}), 404)

    try:
        number.update_number(**data)
        number.save_number()
        return make_response(jsonify({"message": "Number Updated", "data": number.number_json()}), 200)
    except:
        return make_response(jsonify({"message": "Internal Error", "data": {}}), 500)


def get_number(number_id):

    number = ModelNumber.find_number(number_id)

    if not number:
        return make_response(jsonify({"message": "Number not found", "data": {}}), 404)
    return make_response(jsonify({"message": "Number found", "data": number.number_json()}), 200)


def delete_number(number_id):

    number = ModelNumber.find_number(number_id)

    if not number:
        return make_response(jsonify({"message": "Number not found", "data": {}}), 404)

    try:
        number.delete_number()
        return make_response(jsonify({"message": "Number deleted", "data": number.list_json()}), 200)

    except:
        return make_response(jsonify({"message": "Internal Error", "data": {}}), 500)
