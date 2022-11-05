from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return dict(
            id = self.task_id,
            title = self.title,
            description = self.description,
            is_complete = False
        )

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title = task_data["title"],
            description = task_data["description"],
            completed_at = None
        )

    def true_dict(self):
        return dict(
            id = self.task_id,
            title = self.title,
            description = self.description,
            is_complete = True
        )