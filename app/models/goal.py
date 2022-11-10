from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    #task_id = db.Column(db.Integer, db.ForeignKey(task.id))
    #task = db.relationship("Task", back_populates="goals")

    def to_dict(self):
            goal_as_dict = {}
            goal_as_dict["id"] = self.id
            goal_as_dict["title"] = self.title

            return goal_as_dict


    @classmethod
    def from_dict(cls, request_body):
        return Goal(
            title=request_body["title"],
        )