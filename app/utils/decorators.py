__all__ = (
    'json_resp',
)
from flask import jsonify


def json_resp(func):
    def wrapper(*args, **kwargs):
        res = func()
        if isinstance(res, (list, dict, tuple)):
            res = jsonify(res)

        return res

    return wrapper
