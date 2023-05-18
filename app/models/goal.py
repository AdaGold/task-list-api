from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    tasks = db.relationship("Task", back_populates="goal", lazy=True)
    
    @classmethod
    def from_dict(cls, goal_data):

        new_goal = Goal(
        title=task_data["title"],
    )
    
        return new_goal

    def to_dict(self):
        return {
                'id': self.goal_id,
                'title': self.title
            }