from flask import current_app
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable = False)
    description = db.Column(db.String(300))
    completed_at = db.Column(db.DateTime)

    def to_dict(self):
        is_complete = False if self.completed_at is None else True
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }
