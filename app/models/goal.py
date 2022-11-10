from app import db

# One Side
class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', back_populates="goal",lazy=True)

    def to_dict(self):
        result = {
            "id": self.goal_id,
            "title": self.title
            }
        return result

    def to_dict_with_goal_id(self):
        result = {
            "id": self.goal_id,
            "title": self.title,
            "tasks": self.get_tasks_list()
        }
        return result

    def get_tasks_list(self):
        list_of_tasks = []
        for item in self.tasks:
            list_of_tasks.append(item.to_dict())
        return list_of_tasks
    
    @classmethod
    def from_dict(cls, task_dict):
        return cls(
            title=task_dict["title"]
        )