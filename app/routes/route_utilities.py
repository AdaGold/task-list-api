from flask import abort, make_response, Response
from app.db import db


def validate_model(model, model_id):
    if type(model_id) is not int:
        abort(make_response(
            {"details": "Invalid ID"}, 400
        ))

    query = db.select(model).where(model.id == model_id)
    instance = db.session.scalar(query)

    if instance is None:
        abort(make_response(
            {"details": f"{model.__name__} not found"}, 404
        ))

    return instance


def create_model(model, request_body):
    if not isinstance(request_body, dict):
        abort(make_response(
            {"details": "Invalid data"}, 400
        ))

    if not request_body.get("title"):
        abort(make_response(
            {"details": "Invalid data"}, 400
        ))

    if model.__name__ == "Task":
        if "description" not in request_body:
            abort(make_response(
                {"details": "Invalid data"}, 400
            ))

    instance = model.from_dict(request_body)

    db.session.add(instance)
    db.session.commit()

    return instance.to_dict(), 201


def update_model(obj, data):
    for attr, value in data.items():
        if hasattr(obj, attr):
            setattr(obj, attr, value)

    db.session.commit()

    return Response(status=204, mimetype="application/json")
