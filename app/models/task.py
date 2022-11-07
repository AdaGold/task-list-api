from app import db
from flask import make_response, abort


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)

    def to_json(self):
        if self.completed_at:
            is_complete = True
        else:
            is_complete = False

        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }

    @classmethod
    def from_json(cls, request_body):
        return cls(
            title=request_body["title"],
            description=request_body["description"],
            # completed_at=request_body["completed_at"] # Why do I havce to comment this out? 
        )
    
    def update(self,request_body):
        try:
            self.title = request_body["title"]
            # self.completed_at = request_body["completed_at"] # why does this need to be commented out to pass test_update_task ????
            self.description = request_body["description"]
        except KeyError as error:
            abort(make_response({'message': f"Missing attribute: {error}"}))
    
    @classmethod
    def create(cls, request_body):
        new_task = cls(
            title = request_body["title"],
            description = request_body["description"], 
            completed_at = request_body["completed_at"]
        )
            
        return new_task


