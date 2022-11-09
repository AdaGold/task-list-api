from app import db
from flask import Blueprint, jsonify, abort, make_response, request


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    # task_id = db.Column(db.Integer, db.ForeignKey("task.task_id"))
    tasks = db.relationship("Task", back_populates="goal", lazy = True)


    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }


    @classmethod
    def from_dict(cls, request_body):
        

        return cls(
            name=request_body["title"]
        )

  



   
    # def task_to_dict(self):
    #     tasks = self.tasks
    #     task_ids = [task.task_id for task in tasks]

    #     return {
    #         "id": self.goal_id,
    #         "task_ids": task_ids
    #     }