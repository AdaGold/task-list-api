from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable = True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.task_id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        if self.completed_at == None:
            task_as_dict["is_complete"] = False
        else:
            task_as_dict["is_complete"] = True
        
        return task_as_dict

    def to_dict_with_goal(self):
        task_as_dict = self.to_dict()
        task_as_dict["goal_id"] = self.goal_id

        return task_as_dict

    @classmethod
    def from_dict(cls, task_data):
        if not task_data.get("completed_at", None):
            new_task = Task(title=task_data["title"],
                        description=task_data["description"])
        else:
            new_task = Task(title=task_data["title"],
                            description=task_data["description"],
                            completed_at=task_data["completed_at"])
        return new_task