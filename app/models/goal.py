from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)

    def from_dict(self):
        pass

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }
