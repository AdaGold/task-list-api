from app import db
from flask import abort, make_response


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    is_complete = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")


    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.task_id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = self.is_complete

        if self.goal_id:
            task_as_dict["goal_id"] = self.goal_id
            
        return task_as_dict

        
    @classmethod
    def from_dict(cls, request_body):
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"])
        return new_task

   