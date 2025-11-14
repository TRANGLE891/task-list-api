from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'task_ids': [task.id for task in self.tasks],
            'tasks': [ task.to_dict() for task in self.tasks]
        }

    def to_summary_dict(self):
        dictionary = {"id": self.id, "title": self.title}
        return dictionary

    @classmethod
    def from_dict(cls, dict_data: dict):
        goal = Goal(
            id=dict_data.get("id"),
            title=dict_data["title"],
        )
        return goal
    
