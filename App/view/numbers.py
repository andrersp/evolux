# -*- coding: utf-8 -*-

from flask import jsonify, request, make_response
from flask_jwt_extended import jwt_required

from wraps import required_params

from model.numbers import ModelNumber
from model.tables import ModelTable


schema = {
    "id": {"required": True, "nullable": True},
    "value": {"required": True, "type": "string",
              'regex': '^[0-9]{13}$'
              },
    "monthy_price": {"required": True, "type": "float"},
    "setup_price": {"required": True, "type": "float"},
    "currency": {"required": True, "type": "string"},
    "available": {"required": True, "type": "boolean"},
    "table_id": {"required": True, "type": "integer"}
}


@jwt_required
def get_numbers():

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 20))

    query = ModelNumber.query.paginate(page, limit, error_out=False)
    data = [number.list_json() for number in query.items]

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


@ jwt_required
@ required_params(schema)
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


@ jwt_required
@ required_params(schema)
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


@ jwt_required
def get_number(number_id):

    number = ModelNumber.find_number(number_id)

    if not number:
        return make_response(jsonify({"message": "Number not found", "data": {}}), 404)
    return make_response(jsonify({"message": "Number found", "data": number.number_json()}), 200)


@ jwt_required
def delete_number(number_id):

    number = ModelNumber.find_number(number_id)

    if not number:
        return make_response(jsonify({"message": "Number not found", "data": {}}), 404)

    try:
        number.delete_number()
        return make_response(jsonify({"message": "Number deleted", "data": number.list_json()}), 200)

    except:
        return make_response(jsonify({"message": "Internal Error", "data": {}}), 500)
