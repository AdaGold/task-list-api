from flask import jsonify, abort, make_response

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

# def to_dict(obj):
#     attributes = [a for a in dir(obj) if not a.startswith('__')]
#     obj_dict = {}
#     for attribute in attributes:
#         obj_dict[attribute] = obj.attribute
#     return obj_dict
