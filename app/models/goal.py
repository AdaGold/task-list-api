from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)

    def to_dict(self):
        result = {
            "id": self.task_id,
            "title": self.title
            }

        return result
    
    @classmethod
    def from_dict(cls, task_dict):
        return cls(
            title=task_dict["title"]
        )