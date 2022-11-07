from app import db
import datetime


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)

def to_dict(self):
    task_as_dict = {}
    task_as_dict["id"] = self.id
    task_as_dict["title"] = self.title
    task_as_dict["description"] = self.description
    task_as_dict["completed_at"]= self.completed_at 

def from_dict(cls, task_data):
    new_task = Task(
        title=task_data["title"],
        description=task_data["description"],
        completed_at=task_data["is_complete"] # or completed_at???#
    )
    return new_task