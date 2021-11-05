from flask import current_app
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"))
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        is_complete = False if not self.completed_at else True

        response = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete,
        }

        if self.goal:
            response["goal_id"] = self.goal_id
        return response

    def update(self, request_body):
        for key, value in request_body.items():
            if key in Task.__table__.columns.keys():
                setattr(self, key, value)
