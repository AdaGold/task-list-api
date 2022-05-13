from app import db
# from sqlalchemy.sql import func


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    is_complete = db.Column(db.Boolean, nullable=True, default=False)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        goal_title = self.goal.title if self.goal else ""
        goal_id_rec = self.goal.id if self.goal else ""

        task_dict = dict(
            id = self.id,
            title = self.title,
            description = self.description,
            is_complete = self.is_complete,
            completed_at = self.completed_at,
            goal = goal_title,
            goal_id = goal_id_rec
        )
        return task_dict



    @classmethod
    def from_dict(cls, data_dict):
        if "is_complete" not in data_dict and "completed_at" not in data_dict:
            return cls(
                title = data_dict["title"],
                description = data_dict["description"]
            )
        elif "completed_at" in data_dict:
            return cls(
                title = data_dict["title"],
                description = data_dict["description"],
                is_complete = True,
                completed_at = data_dict["completed_at"]
            )
        # else:
        #     return cls(
        #         title = data_dict["title"],
        #         description = data_dict["description"],
        #         completed_at = data_dict["completed_at"],
        #         is_complete = True,

        #     )


    # @classmethod
    # def from_dict(cls, data_dict):
    #     complete_dict = {k:v for k,v in data_dict.items()}
    #     if "is_complete" not in data_dict:
    #         complete_dict["is_complete"] = False
    #     if "completed_at" not in data_dict:
    #         complete_dict["completed_at"] = None

    #     return cls(
    #         title = complete_dict["title"],
    #         description = complete_dict["description"],
    #         is_complete = complete_dict["is_complete"],
    #         completed_at = complete_dict["completed_at"]
    #     )