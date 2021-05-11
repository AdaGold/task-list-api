from flask import current_app
from app import db
from flask import jsonify

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)

    def is_complete(self):
        if self.completed_at is None:
            return False
        else:
            return True

    def to_dict(self):
        task = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete()
            }
        if self.goal:
            task["goal_id"] = self.goal_id
        return task
