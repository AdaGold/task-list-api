from app import db
from flask import abort, make_response


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    @classmethod
    def create(cls, request_body):
        new_goal = cls(
            title = request_body["title"],
        )   
        return new_goal

    def update(self,request_body):
        try:
            self.title = request_body["title"]
        except KeyError as error:
            abort(make_response({'message': f"Missing attribute: {error}"}))

    def to_json(self):
        return {
            "id": self.goal_id,
            "title": self.title,
        }
