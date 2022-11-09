from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")


    def to_dict(self):
        
        if self.goal_id:
            return {
            "id": self.task_id,
            "goal_id":self.goal_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete()
        }
            
        else:
            return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete()
        }
        
    def is_complete(self):
        return self.completed_at != None

    @classmethod
    def from_dict(cls, request_body):
        return cls(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body.get["completed_at"])
