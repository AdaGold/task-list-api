from flask import current_app
from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250))
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    @classmethod
    def from_dict(cls, goal_dict):
        return cls(**goal_dict)

    def to_dict(self, tasks=False):
        goal_dict = {
            "id": self.id,
            "title": self.title,
        }
        if tasks:
            goal_dict.update({"tasks": [task.to_dict() for task in self.tasks]})

        return goal_dict
