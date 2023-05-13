from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    # establishes the one-to-many relationship
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        if self.completed_at:
            completed = True
        else:
            completed = False

        task_as_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": completed,
        }

        if self.goal_id:
            task_as_dict["goal_id"] = self.goal_id

        return task_as_dict

    @classmethod
    def from_dict(cls, task_data):
        """Takes in a dictionary and returns a new Task instance"""
        new_task = Task(title=task_data["title"],
                        description=task_data["description"])
        return new_task
