# -*- coding: utf-8 -*-

from flask import jsonify, make_response, request

from model.users import ModelUser

from wraps import required_params

schema = {
    "id": {"required": True, "nullable": True},
    "username": {"type": "string", "required": True},
    "password": {"type": "string", "required": True},
    "active": {"type": "boolean", "required": True}
}


def get_users():

    data = [user.user_json() for user in ModelUser.query.all()]

    return make_response(jsonify({"data": data}), 200)


def get_user(id_user):

    user = ModelUser.find_user(id_user)

    if not user:
        return make_response(jsonify({"message": "User not found", "data": {}}), 404)

    return make_response(jsonify({"message": "User Found", "data": user.user_json()}), 200)


@required_params(schema)
def save_user():
    data = request.json

    user = ModelUser.find_user(data.get("id"))

    if user:
        return update_user()

    username = ModelUser.find_username(data.get("username"))

    if username:
        return make_response(jsonify(
            {"message": "Username already exists. Try another one.",
             "data": {}}), 400)

    try:
        user = ModelUser(**data)
        user.hash_password()
        user.save_user()

        return make_response(jsonify({"message": "New User Saved", "data": user.user_json()}), 201)

    except:
        make_response(
            jsonify({"message": "Internal error", "data": "{}"}), 500)


@required_params(schema)
def update_user():
    data = request.json

    user = ModelUser.find_user(data.get("id"))

    username = ModelUser.find_username(data.get("username"))

    if username:
        if data.get("id") != str(username.id_user):
            return make_response(jsonify(
                {"message": "Username already exists. Try another one.",
                 "data": {}}), 400)

    try:

        user.update_user(**data)
        user.hash_password()
        user.save_user()

        return make_response(jsonify({"message": "User Updated", "data": user.user_json()}), 200)
    except:
        return make_response(jsonify({"message": "Internal Error", "data": {}}), 500)
