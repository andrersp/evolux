# -*- coding: utf-8 -*-

from flask import jsonify, make_response, request
from flask_jwt_extended import create_access_token, jwt_required


from model.users import ModelUser

from wraps import required_params

schema = {
    "id": {"required": True, "nullable": True},
    "username": {"type": "string", "required": True},
    "password": {"type": "string", "required": True},
    "active": {"type": "boolean", "required": True}
}


@jwt_required
def get_users():

    data = [user.user_json() for user in ModelUser.query.all()]

    return make_response(jsonify({"data": data}), 200)


@jwt_required
def get_user(id_user):

    user = ModelUser.find_user(id_user)

    if not user:
        return make_response(jsonify({"message": "User not found", "data": {}}), 404)

    return make_response(jsonify({"message": "User Found", "data": user.user_json()}), 200)


@jwt_required
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


@jwt_required
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


schema = {
    "username": {"type": "string", "required": True},
    "password": {"type": "string", "required": True}
}


@required_params(schema)
def user_login():

    dados = request.json

    user = ModelUser.find_username(dados.get("username"))

    if not user:
        return make_response(jsonify(
            {"message": "Username not found.",
             "data": {}}), 400)

    if not user.check_password(dados.get("password")):
        return make_response(jsonify(
            {"message": "Password does not match.",
             "data": {}}), 400)
    if not user.active:
        return make_response(jsonify(
            {"message": "User is disabled.",
             "data": {}}), 400)

    token = create_access_token(identity=user.id_user)

    return make_response(jsonify({"message": "Login Success", "data": {
        "token": token
    }}), 200)
