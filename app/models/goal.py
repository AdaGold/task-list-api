from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }

    @classmethod
    def from_dict(cls, request_body):
        return cls(
            title=request_body["title"]
        )

    def update(self, req_body):
        try: 
            self.title = req_body["title"]
        except KeyError as error:
            abort(make_response({'message': f"Missing attribute: {error}"}))