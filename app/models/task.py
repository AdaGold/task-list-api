from app import db
from datetime import datetime


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    goal = db.relationship("Goal", back_populates="tasks")


    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"]= bool(self.completed_at)

        return task_as_dict


    @classmethod
    def from_dict(cls, request_body):
        return Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=None
        )