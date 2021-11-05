from flask import current_app
from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self, has_tasks=False):
        response = {
            "id": self.id,
            "title": self.title,
        }

        if has_tasks:
            response["tasks"] = [task.to_dict() for task in self.tasks]

        return response

    def update(self, request_body):
        for key, value in request_body.items():
            if key in Goal.__table__.columns.keys():
                setattr(self, key, value)
