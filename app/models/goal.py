from flask import current_app
from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))

    @classmethod
    def from_dict(cls, goal_dict):
        return cls(**goal_dict)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }
