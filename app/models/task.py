from flask import current_app, jsonify
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)

    def to_dict(self):
        task = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
        }
        
        if self.goal_id:
            task["goal_id"] = self.goal_id

        return task


