from functools import wraps

from flask import request, jsonify, make_response

from cerberus import Validator


def required_params(schema):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):

            try:
                data = request.json
            except:
                data = {}

            v = Validator(schema)
            v.allow_unknown = False

            if not v.validate(data):
                response = make_response(jsonify({"message": v.errors}), 400)

                response.headers["Content-Type"] = "application/json"
                return response
            return fn(*args, **kwargs)
        return wrapper
    return decorator
