from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    #tasks = db.realtionship("Task", back_populates="goal")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }
    
    @classmethod
    def from_dict(cls, goal_data):
        new_goal = cls(
            title = goal_data["title"]
        )
        return new_goal