from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        if not self.completed_at:
            is_complete = False
        else:
            is_complete = True
        return {
            "id": self.id,
            "goal_id": self.goal_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }

    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(
            title = task_data["title"],
            description = task_data["description"],
            completed_at = task_data["completed_at"]
        )
        return new_task

