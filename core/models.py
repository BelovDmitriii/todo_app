from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    priority = Column(Integer, default=2)
    done = Column(Boolean, default=False)
    position = Column(Integer, default=0)

    def __repr__ (self):
        return f"<Task(id={self.id}, title='{self.title}', done={self.done})>"

    def toggle_status(self):
        self.done = not self.done

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "done": self.done,
            "position": self.position
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data["title"],
            priority=data.get("priority", 2),
            done=data.get("done", False),
            position=data.get("position", 0)
        )

    def __str__(self):
        status = "✅" if self.done else "🔲"
        icon = {3: "🔥", 2: "⚠️", 1: "📝"}.get(self.priority, "")
        return f"{status} {icon} {self.title}"

    def __repr__(self):
        return f"<Task id={self.id} title='{self.title}' priority={self.priority} status={self.status}>"
