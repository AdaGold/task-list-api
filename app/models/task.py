from flask import current_app
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(300))
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    @classmethod
    def from_dict(cls, task_dict):
        return cls(**task_dict)

    def to_dict(self):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.get_status()
        }
        if self.goal_id:
            task_dict.update({"goal_id": self.goal_id})
        return task_dict

    def get_status(self):
        return False if self.completed_at is None else True

    def edit(self, task_dict):
        for attribute, value in task_dict.items():
            if hasattr(self, attribute):
                setattr(self, attribute, value)
