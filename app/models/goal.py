from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str | None]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'task_ids': [task.id for task in self.tasks],
            'tasks': [ task.to_dict() for task in self.tasks]
        }

    def to_summary_dict(self):
        dictionary = {"id": self.id, "title": self.title}
        if (self.description):
            dictionary['description'] = self.description
        return dictionary

    @classmethod
    def from_dict(cls, dict_data: dict):
        goal = Goal(
            id=dict_data.get("id"),
            title=dict_data["title"],
            description=dict_data.get("description"),
        )
        return goal
    
