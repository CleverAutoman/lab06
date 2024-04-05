from db import db

class TaskModel(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True, nullable=False)
    is_completed = db.Column(db.Boolean, unique=False, nullable=True, default=False)

