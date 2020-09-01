# -*- coding: utf-8 -*-

from flask import jsonify, make_response, request
from wraps import required_params

from model.tables import ModelTable


schema = {
    "table_id": {"required": True, "nullable": True},
    "name": {"type": "string", "required": True, "maxlength": 80},
    "max_line": {"type": "integer", "required": True}
}


def get_tables():

    data = [table.list_json() for table in ModelTable.query.all()]

    respose = make_response(jsonify({"data": data}), 200)
    return respose


@required_params(schema)
def save_table():

    data = request.json

    table = ModelTable.find_table(data.get("table_id"))

    if table:
        return update_table()

    try:
        # print(data)
        table = ModelTable(**data)
        table.save_table()

        return make_response(jsonify({"message": "New Table Saved", "data": table.list_json()}), 201)
    except:
        return make_response(jsonify({"message": "Internal Error", "data": table.list_json()}), 500)


@required_params(schema)
def update_table():
    data = request.json
    table = ModelTable.find_table(data.get("table_id"))

    try:
        table.update_table(**data)
        table.save_table()
        return make_response(jsonify({"message": "Table Updated", "data": table.list_json()}), 200)

    except:
        return make_response(jsonify({"message": "Internal Error", "data": {}}), 500)


def get_table(table_id):

    table = ModelTable.find_table(table_id)

    if not table:
        return make_response(jsonify({"message": "Table not found", "data": {}}), 404)

    return make_response(jsonify({"message": "Table found", "data": table.list_json()}), 200)


def delete_table(table_id):

    table = ModelTable.find_table(table_id)

    if not table:
        return make_response(jsonify({"message": "Table not found", "data": {}}), 404)

    try:
        table.delete_table()
        return make_response(jsonify({"message": "Table deleted", "data": table.list_json()}), 200)
    except:
        return make_response(jsonify({"message": "Internal Error", "data": {}}), 500)
