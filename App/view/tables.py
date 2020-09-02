# -*- coding: utf-8 -*-

from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required
from wraps import required_params

from model.tables import ModelTable


schema = {
    "table_id": {"required": True, "nullable": True},
    "name": {"type": "string", "required": True, "maxlength": 80},
    "max_line": {"type": "integer", "required": True}
}


@jwt_required
def get_tables():

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 20))

    query = ModelTable.query.paginate(page, limit, error_out=False)

    data = [table.list_json() for table in query.items]
    previus = "" if not query.has_prev else "{}?page={}&limit={}".format(
        request.base_url, query.prev_num, limit)

    if query.page > query.pages:
        return make_response(jsonify({"message": "Page out range", "previus": "{}?page={}&limit={}".format(
            request.base_url, query.pages, limit)}), 404)

    next = "" if not query.has_next else "{}?page={}&limit={}".format(
        request.base_url, query.next_num, limit)

    respose = make_response(jsonify({
        "data": data,
        "page": "{} of {}".format(query.page, query.pages),
        "items": "{} of {}".format(query.per_page, query.total),
        "previous": previus,
        "next": next
    }
    ), 200)
    return respose


@jwt_required
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


@jwt_required
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


@jwt_required
def get_table(table_id):

    table = ModelTable.find_table(table_id)

    if not table:
        return make_response(jsonify({"message": "Table not found", "data": {}}), 404)

    return make_response(jsonify({"message": "Table found", "data": table.table_json()}), 200)


@jwt_required
def delete_table(table_id):

    table = ModelTable.find_table(table_id)

    if not table:
        return make_response(jsonify({"message": "Table not found", "data": {}}), 404)

    try:
        table.delete_table()
        return make_response(jsonify({"message": "Table deleted", "data": table.list_json()}), 200)
    except:
        return make_response(jsonify({"message": "Internal Error", "data": {}}), 500)
