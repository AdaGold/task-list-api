from app import db
class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String)
    description=db.Column(db.Text)
    completed_at=db.Column(db.DateTime,nullable=True)
    goal_id=db.Column(db.Integer,db.ForeignKey("goal.id"))
    goal=db.relationship("Goal",back_populates="tasks")

    @classmethod
    def from_dict(cls,req_body):
        return cls(title=req_body['title'],
        description=req_body['description'],)
        #completed_at=req_body['completed_at'])

    def to_dict(self):
        task_as_dict={}
        task_as_dict["description"]=self.description
        task_as_dict["id"]=self.id
        task_as_dict["title"]=self.title
        task_as_dict["is_complete"]=bool(self.completed_at)
        
        if self.goal_id:
            task_as_dict["goal_id"]=self.goal_id
        return task_as_dict
        
        #return task_as_dict
    def task_goal_dict(self):
        task_as_dict={}
        task_as_dict["description"]=self.description
        task_as_dict["id"]=self.id
        task_as_dict["title"]=self.title
        task_as_dict["is_complete"]=bool(self.completed_at)
        task_as_dict["goal_id"]=self.goal_id
        return task_as_dict

        