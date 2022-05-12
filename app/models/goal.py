from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)

    def to_dict(self):
        goal_dict = dict(
            id = self.id,
            title = self.title,
        )
        return goal_dict

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title = data_dict["title"]
        )