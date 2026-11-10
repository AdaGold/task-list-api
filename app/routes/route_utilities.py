from flask import abort, jsonify
from werkzeug.exceptions import BadRequest, NotFound
from app.db import db


class JSONBadRequest(BadRequest):
    def get_body(self, environ=None, scope=None):
        return jsonify({
            "details": self.description
        }).get_data(as_text=True)

    def get_headers(self, environ=None, scope=None):
        return [("Content-Type", "application/json")]
    
class JSONNotFound(NotFound):
    def get_body(self, environ=None, scope=None):
        return jsonify({
            "details": self.description
        }).get_data(as_text=True)

    def get_headers(self, environ=None, scope=None):
        return [("Content-Type", "application/json")]

def validate_model(model, model_id):
    if type(model_id) is not int:
        raise JSONBadRequest(description="Invalid ID")

    instance = db.session.get(model, model_id)

    if instance is None:
        raise JSONNotFound(
            description=f"{model.__name__} not found"
        )

    return instance


def create_model(model, request_body):
    if not isinstance(request_body, dict):
        raise JSONBadRequest(description="Invalid data")

    if not request_body.get("title"):
        raise JSONBadRequest(description="Invalid data")

    if model.__name__ == "Task":
        if "description" not in request_body:
            raise JSONBadRequest(description="Invalid data")

    instance = model.from_dict(request_body)

    db.session.add(instance)
    db.session.commit()

    return instance.to_dict(), 201

