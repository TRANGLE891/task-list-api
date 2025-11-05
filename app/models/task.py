from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[str | None]

    @classmethod
    def from_dict(cls, dict_data: dict):
        task = Task(
            id=dict_data.get("id"),
            title=dict_data["title"],
            description=dict_data["description"],
            completed_at=dict_data.get("completed_at")
        )
        return task
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'is_complete': self.completed_at is not None,
        }