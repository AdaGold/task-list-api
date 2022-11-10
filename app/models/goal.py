from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String)
    tasks=db.relationship("Task",back_populates="goal",lazy=True)

    @classmethod
    def from_dict(cls,req_body):
        return cls(title=req_body['title'])

    def to_dict(self):
        goal_as_dict={}
        goal_as_dict["id"]=self.id
        goal_as_dict["title"]=self.title
        return goal_as_dict


