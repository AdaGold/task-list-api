from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String)

    @classmethod
    def from_dictg(cls,req_body):
        return cls(title=req_body['title'])

    def to_dictg(self):
        goal_as_dict={}
        goal_as_dict["id"]=self.id
        goal_as_dict["title"]=self.id
        return goal_as_dict


