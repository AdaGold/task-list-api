# from datetime import datetime
# from sqlalchemy import DateTime
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)


    def is_complete(self):

        is_complete = None
        if self.completed_at is None:
            is_complete = False
        else:
            is_complete = True
        return is_complete


    @classmethod
    def dict_for_post_method(cls, tasks_details):

        result = cls(
            title=tasks_details["title"],
            description=tasks_details["description"],
            completed_at=None)
        return result
    

    def to_dict(self):
        return \
            {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete()
            }